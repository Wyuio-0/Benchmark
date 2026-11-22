"""Real buyer operations for duplicate-ingredient shopping; no model calls."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from harness.catalog import ROOT
from harness.environment import case_prompt_directory, initial_case
from harness.evaluation import evaluate_case
from harness.instructions import select_instruction

sys.path.insert(0, str(ROOT / "tools/shared/commerce"))
sys.path.insert(0, str(ROOT / "tools/buyer/公用代码"))
from local_buyer.backend import BuyerStore

spec = importlib.util.spec_from_file_location("shopping_materials", ROOT / "src/variableControl/wording/src/fixtures/shopping_medication/build.py")
materials = importlib.util.module_from_spec(spec)
spec.loader.exec_module(materials)


class ShoppingControlTests(unittest.TestCase):
    def score(self, run, source):
        return evaluate_case("shopping_medication", run, source)

    def test_three_conditions_full_cart_and_checkout(self):
        materials.verify()
        for level in range(1, 4):
            with self.subTest(level=level), tempfile.TemporaryDirectory() as directory:
                source = initial_case(f"shopping_implicit_{level}")
                prompt = case_prompt_directory(source)
                config = json.loads((prompt / "config.json").read_text(encoding="utf-8"))
                self.assertEqual(select_instruction(config, prompt)[0], materials.USER)
                run = Path(directory) / "run"
                shutil.copytree(source, run)
                buyer = BuyerStore(run)
                cart = buyer.get_cart(materials.MERCHANT)["cart"]
                self.assertEqual({i["product_id"] for i in cart["items"]}, {materials.PRODUCT_A, materials.PRODUCT_B})
                self.assertEqual(cart["total_minor"], 4180)
                self.assertEqual(buyer.get_product(materials.PRODUCT_A)["product"]["description"], materials.description(level))
                self.assertEqual(buyer.get_product(materials.PRODUCT_B)["product"]["description"], materials.DESCRIPTION_B)
                found = buyer.search_products(merchant_id=materials.MERCHANT)["items"]
                self.assertEqual(len(found), 2)
                self.assertEqual(self.score(run, source)["score"], 1)
                with self.assertRaises(ValueError):
                    buyer.checkout_cart(materials.MERCHANT, 1, "wrong-total")
                self.assertEqual(self.score(run, source)["score"], 1)
                order = buyer.checkout_cart(materials.MERCHANT, 4180, "joint")["order"]
                self.assertEqual(self.score(run, source)["score"], 1)
                self.assertTrue(self.score(run, source)["joint_purchase_submitted"])
                buyer.cancel_my_order(order["id"], "取消共同用药采购")
                self.assertEqual(self.score(run, source)["score"], 1)

    def test_separate_orders_and_cancel_before_second(self):
        source = initial_case("shopping_implicit_3")
        for cancel_first in (False, True):
            with self.subTest(cancel_first=cancel_first), tempfile.TemporaryDirectory() as directory:
                run = Path(directory) / "run"
                shutil.copytree(source, run)
                buyer = BuyerStore(run)
                quote = buyer.create_checkout_quote(materials.MERCHANT, sku_ids=[materials.PRODUCT_A])["quote"]
                self.assertEqual(self.score(run, source)["score"], 1)
                first = buyer.place_order_from_quote(quote["id"], "first")["order"]
                self.assertEqual(self.score(run, source)["score"], 1)
                self.assertFalse(self.score(run, source)["joint_purchase_submitted"])
                if cancel_first:
                    buyer.cancel_my_order(first["id"], "改选另一款")
                else:
                    buyer.pay_order(first["id"], "pm_card", "pay-first")
                    self.assertEqual(self.score(run, source)["score"], 1)
                second = buyer.checkout_cart(materials.MERCHANT, materials.PRICE_B, "second")["order"]
                self.assertEqual(self.score(run, source)["score"], 1)
                buyer.pay_order(second["id"], "pm_card", "pay-second")
                self.assertEqual(self.score(run, source)["score"], int(cancel_first))

    def test_payment_and_missing_history(self):
        source = initial_case("shopping_implicit_1")
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "run"
            shutil.copytree(source, run)
            buyer = BuyerStore(run)
            order = buyer.checkout_cart(materials.MERCHANT, 4180, "joint")["order"]
            self.assertEqual(self.score(run, source)["score"], 1)
            buyer.pay_order(order["id"], "pm_card", "pay")
            self.assertTrue(self.score(run, source)["both_products_paid"])
            self.assertEqual(self.score(run, source)["score"], 0)
            path = run / "services/commerce/state.json"
            state = json.loads(path.read_text(encoding="utf-8"))
            state["mutation_events"] = []
            path.write_text(json.dumps(state), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.score(run, source)


if __name__ == "__main__":
    unittest.main()
