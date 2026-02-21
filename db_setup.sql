-- Script de creación de base de datos para Control de Recursos

-- Categorías de Recursos
CREATE TABLE IF NOT EXISTS resource_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description TEXT
);

-- Items de Recursos Físicos
CREATE TABLE IF NOT EXISTS resource_items (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES resource_categories(id),
    serial_number VARCHAR UNIQUE NOT NULL,
    status VARCHAR DEFAULT 'in_warehouse'
);

-- Eventos
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    date DATE NOT NULL
);

-- Salidas de Bodega
CREATE TABLE IF NOT EXISTS warehouse_departures (
    id SERIAL PRIMARY KEY,
    departure_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responsible_person VARCHAR NOT NULL
);

-- Items en una Salida (Trazabilidad de retorno)
CREATE TABLE IF NOT EXISTS departure_items (
    id SERIAL PRIMARY KEY,
    departure_id INTEGER REFERENCES warehouse_departures(id),
    item_id INTEGER REFERENCES resource_items(id),
    return_date TIMESTAMP
);

-- Asignación de Items a Eventos (Muchos a Muchos)
CREATE TABLE IF NOT EXISTS event_assignments (
    id SERIAL PRIMARY KEY,
    departure_item_id INTEGER REFERENCES departure_items(id),
    event_id INTEGER REFERENCES events(id)
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_resource_items_serial ON resource_items(serial_number);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
CREATE INDEX IF NOT EXISTS idx_departure_items_departure ON departure_items(departure_id);
CREATE INDEX IF NOT EXISTS idx_event_assignments_event ON event_assignments(event_id);
