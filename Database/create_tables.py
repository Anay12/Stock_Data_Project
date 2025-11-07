from Database.database import Base, engine

""" Creates all tables defined in models.py """

Base.metadata.create_all(bind=engine)

# with engine.connect() as conn:
#     conn.execute(text("ALTER TABLE holdings ADD COLUMN dateEdited Date"))
#     conn.commit()

print("All tables created!")

