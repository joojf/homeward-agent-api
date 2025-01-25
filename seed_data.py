import json

from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

from app.database import SessionLocal, engine
from app.models import Base, Agent, Application, Customer


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    with open("fixtures/agents.json", "r") as f:
        agents_data = json.load(f)["agents"]
        for a in agents_data:
            agent = Agent(**a)
            db.add(agent)
    db.commit()

    with open("fixtures/customers.json", "r") as f:
        cust_data = json.load(f)["customers"]
        for c in cust_data:
            customer = Customer(**c)
            db.add(customer)
    db.commit()

    with open("fixtures/applications.json", "r") as f:
        apps_data = json.load(f)["applications"]
        for app in apps_data:
            record = {
                "id": app["id"],
                "customer_id": app["customer_id"],
                "purchasing_address": app.get("purchasing_address"),
                "current_address": app.get("current_address"),
                "application_approved": app["application_approved"],
                "agent_id": app["agent"]
            }
            db.add(Application(**record))
    db.commit()

    db.close()


if __name__ == "__main__":
    seed()
