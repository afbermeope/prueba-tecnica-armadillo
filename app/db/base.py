from app.db.session import Base
from app.models.item import Item
from app.models.event import Event, ResourceAssignment
from app.models.person import Person
from app.models.warehouse import Warehouse, WarehouseStock
from app.models.location import Location
from app.models.role import Role
from sqlalchemy.orm import configure_mappers

# Force mapping configuration to resolve string references
configure_mappers()
