-- Personas (Responsables y participantes)
CREATE TABLE IF NOT EXISTS persons (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    identification_number VARCHAR UNIQUE NOT NULL,
    phone VARCHAR,
    email VARCHAR
);

-- Bodegas
CREATE TABLE IF NOT EXISTS warehouses (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    location VARCHAR,
    address VARCHAR
);

-- Catálogo de Recursos Físicos (Definición genérica)
CREATE TABLE IF NOT EXISTS resource_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);

-- Stock en Bodegas (Unidad de medida: Ítem por Bodega)
CREATE TABLE IF NOT EXISTS warehouse_stocks (
    id SERIAL PRIMARY KEY,
    warehouse_id INTEGER REFERENCES warehouses(id),
    item_id INTEGER REFERENCES resource_items(id),
    quantity INTEGER DEFAULT 0
);

-- Lugares (Sedes para eventos)
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    address VARCHAR,
    city VARCHAR,
    capacity INTEGER
);

-- Eventos
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location_id INTEGER REFERENCES locations(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

-- Participación en Eventos (Entidad intermedia completa)
CREATE TABLE IF NOT EXISTS event_participations (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    person_id INTEGER REFERENCES persons(id),
    role VARCHAR,
    UNIQUE(event_id, person_id)
);

-- Asignación de Recursos (Vinculado a la Participación y al Stock)
CREATE TABLE IF NOT EXISTS resource_assignments (
    id SERIAL PRIMARY KEY,
    participation_id INTEGER REFERENCES event_participations(id),
    warehouse_stock_id INTEGER REFERENCES warehouse_stocks(id),
    assigned_quantity INTEGER NOT NULL,
    serial_number VARCHAR,
    status VARCHAR DEFAULT 'assigned', -- assigned, delivered, returned
    assignment_date DATE DEFAULT CURRENT_DATE,
    delivery_date DATE,
    return_date DATE
);

--Asignacion de stock a eventos
CREATE TABLE IF NOT EXISTS event_warehouse_stocks (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    warehouse_stock_id INTEGER REFERENCES warehouse_stocks(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_resource_items_name ON resource_items(name);
CREATE INDEX IF NOT EXISTS idx_events_dates ON events(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_persons_id_number ON persons(identification_number);
CREATE INDEX IF NOT EXISTS idx_warehouse_stocks_query ON warehouse_stocks(warehouse_id, item_id);
CREATE INDEX IF NOT EXISTS idx_assignments_stock ON resource_assignments(warehouse_stock_id);
CREATE INDEX IF NOT EXISTS idx_assignments_participation ON resource_assignments(participation_id);
CREATE INDEX IF NOT EXISTS idx_participations_event ON event_participations(event_id);
CREATE INDEX IF NOT EXISTS idx_participations_person ON event_participations(person_id);
CREATE INDEX IF NOT EXISTS idx_events_location ON events(location_id);
