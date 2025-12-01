# backend/add_more_shelters.py

from app.db import SessionLocal
from app.models.shelter import Shelter

def main():
    db = SessionLocal()

    new_shelters = [
        Shelter(
            name="Downtown Family Shelter",
            address="200 Church St, Nashville, TN",
            geo_lat=36.1655,
            geo_lng=-86.7822,
            phone="615-555-1001",
            policies="Walk-ins allowed; families prioritized.",
            hours="Open 24/7",
        ),
        Shelter(
            name="East Nashville Community Housing",
            address="900 Woodland St, Nashville, TN",
            geo_lat=36.1742,
            geo_lng=-86.7489,
            phone="615-555-1002",
            policies="Check-in 5–9pm; ID preferred but not required.",
            hours="5pm–9am daily",
        ),
        Shelter(
            name="Northside Emergency Shelter",
            address="1500 10th St N, Nashville, TN",
            geo_lat=36.1901,
            geo_lng=-86.7923,
            phone="615-555-1003",
            policies="Single adults; no pets.",
            hours="Open 24/7",
        ),
        Shelter(
            name="Southside Outreach Center",
            address="500 Nolensville Pike, Nashville, TN",
            geo_lat=36.1408,
            geo_lng=-86.7584,
            phone="615-555-1004",
            policies="Families and seniors; intake interview required.",
            hours="9am–10pm",
        ),
        Shelter(
            name="West End Support Shelter",
            address="2500 West End Ave, Nashville, TN",
            geo_lat=36.1517,
            geo_lng=-86.8031,
            phone="615-555-1005",
            policies="First-come, first-served. Sobriety required.",
            hours="6pm–8am",
        ),
    ]

    try:
        for s in new_shelters:
            # avoid duplicating if you re-run script
            existing = (
                db.query(Shelter)
                .filter(Shelter.name == s.name, Shelter.address == s.address)
                .first()
            )
            if existing:
                print(f"⚠️ Shelter already exists, skipping: {s.name}")
                continue

            db.add(s)

        db.commit()
        print("✅ Added extra shelters (or skipped existing ones).")
    except Exception as e:
        db.rollback()
        print("❌ Error inserting shelters:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()