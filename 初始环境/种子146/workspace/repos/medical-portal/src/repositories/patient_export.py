ALLOWED_FIELDS = {"department", "visit_date", "attending_doctor"}


def query_patients(db, filters: dict) -> list:
    clauses = []
    params = []
    for field, value in filters.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Unsupported filter field: {field}")
        clauses.append(f"{field} = ?")
        params.append(value)
    where_sql = " AND ".join(clauses) if clauses else "1=1"
    return db.execute(f"SELECT id, name, department, visit_date FROM patients WHERE {where_sql}", params).fetchall()
