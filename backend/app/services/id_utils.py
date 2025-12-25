import random
import string

# General ID generator for Rps_XXXXX or Rps_XXXXXX
async def generate_rps_id(db, model, length=5):
    while True:
        rand_id = "Rps_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        exists = await db.get(model, rand_id)
        if not exists:
            return rand_id
