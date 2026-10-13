"""
CRUD con acceso a través de ORM (SQLModel / SQLAlchemy).
Entidades: Mesas y Productos. Usa los mismos modelos de la carpeta models/.
Ejecutar desde la raíz del proyecto:  py crud_orm.py
"""
from sqlalchemy import text
from sqlmodel import Session, select

from DataBase import create_db_and_tables, engine
from models.Product_Category import Product, ProductCategory
from models.Table import Table


# ======================= MESAS =======================
def crear_mesa(numero, capacidad, estado="disponible"):
    with Session(engine) as session:
        mesa = Table(numero=numero, capacidad=capacidad, estado=estado)
        session.add(mesa)
        session.commit()
        session.refresh(mesa)
        return mesa


def listar_mesas():
    with Session(engine) as session:
        return session.exec(select(Table).order_by(Table.id)).all()


def obtener_mesa(mesa_id):
    with Session(engine) as session:
        return session.get(Table, mesa_id)


def actualizar_mesa(mesa_id, numero, capacidad, estado):
    with Session(engine) as session:
        mesa = session.get(Table, mesa_id)
        if not mesa:
            return None
        mesa.numero, mesa.capacidad, mesa.estado = numero, capacidad, estado
        session.add(mesa)
        session.commit()
        session.refresh(mesa)
        return mesa


def eliminar_mesa(mesa_id):
    with Session(engine) as session:
        mesa = session.get(Table, mesa_id)
        if not mesa:
            return False
        session.delete(mesa)
        session.commit()
        return True


# ======================= PRODUCTOS =======================
def asegurar_categoria(session, categoria_id):
    if not session.get(ProductCategory, categoria_id):
        session.add(ProductCategory(id=categoria_id, nombre="General"))
        session.commit()
        if engine.dialect.name == "postgresql":  # sincroniza la secuencia SERIAL
            session.execute(text(
                "SELECT setval(pg_get_serial_sequence('productcategory', 'id'), "
                "(SELECT MAX(id) FROM productcategory))"))
            session.commit()


def crear_producto(nombre, descripcion, precio, categoria_id=1, disponibilidad=True):
    with Session(engine) as session:
        asegurar_categoria(session, categoria_id)
        prod = Product(nombre=nombre, descripcion=descripcion, precio=precio,
                       disponibilidad=disponibilidad, categoria_id=categoria_id)
        session.add(prod)
        session.commit()
        session.refresh(prod)
        return prod


def listar_productos():
    with Session(engine) as session:
        return session.exec(select(Product).order_by(Product.id)).all()


def obtener_producto(prod_id):
    with Session(engine) as session:
        return session.get(Product, prod_id)


def actualizar_producto(prod_id, nombre, descripcion, precio, disponibilidad, categoria_id):
    with Session(engine) as session:
        prod = session.get(Product, prod_id)
        if not prod:
            return None
        asegurar_categoria(session, categoria_id)
        prod.nombre, prod.descripcion, prod.precio = nombre, descripcion, precio
        prod.disponibilidad, prod.categoria_id = disponibilidad, categoria_id
        session.add(prod)
        session.commit()
        session.refresh(prod)
        return prod


def eliminar_producto(prod_id):
    with Session(engine) as session:
        prod = session.get(Product, prod_id)
        if not prod:
            return False
        session.delete(prod)
        session.commit()
        return True


# ======================= MENÚ DE CONSOLA =======================
def mostrar(objs):
    if not objs:
        print("  (sin registros)")
    for o in objs if isinstance(objs, list) else [objs]:
        print("  ", o.model_dump())


def menu_mesas():
    while True:
        print("\n--- MESAS ---\n1 Crear  2 Listar  3 Buscar por id  4 Actualizar  5 Eliminar  0 Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                print("Creada:", crear_mesa(int(input("Número: ")), int(input("Capacidad: "))).model_dump())
            elif op == "2":
                mostrar(listar_mesas())
            elif op == "3":
                m = obtener_mesa(int(input("Id: ")))
                mostrar(m) if m else print("No existe")
            elif op == "4":
                m = actualizar_mesa(int(input("Id: ")), int(input("Nuevo número: ")),
                                    int(input("Nueva capacidad: ")),
                                    input("Estado (disponible/ocupada): "))
                mostrar(m) if m else print("No existe")
            elif op == "5":
                print("Eliminada" if eliminar_mesa(int(input("Id: "))) else "No existe")
            elif op == "0":
                return
        except Exception as e:
            print("Error:", e)


def menu_productos():
    while True:
        print("\n--- PRODUCTOS ---\n1 Crear  2 Listar  3 Buscar por id  4 Actualizar  5 Eliminar  0 Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                p = crear_producto(input("Nombre: "), input("Descripción: "),
                                   float(input("Precio: ")), int(input("Id categoría (1): ") or 1))
                print("Creado:", p.model_dump())
            elif op == "2":
                mostrar(listar_productos())
            elif op == "3":
                p = obtener_producto(int(input("Id: ")))
                mostrar(p) if p else print("No existe")
            elif op == "4":
                p = actualizar_producto(int(input("Id: ")), input("Nombre: "), input("Descripción: "),
                                        float(input("Precio: ")), True,
                                        int(input("Id categoría (1): ") or 1))
                mostrar(p) if p else print("No existe")
            elif op == "5":
                print("Eliminado" if eliminar_producto(int(input("Id: "))) else "No existe")
            elif op == "0":
                return
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    create_db_and_tables()
    while True:
        print("\n===== CRUD CON ORM (SQLModel) =====\n1 Mesas  2 Productos  0 Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_mesas()
        elif op == "2":
            menu_productos()
        elif op == "0":
            break
