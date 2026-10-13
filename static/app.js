const API_URL = window.location.origin;

// Cargar Lista de Productos en el Menú
async function cargarMenu() {
    try {
        const res = await fetch(`${API_URL}/mesero/menu`);
        const productos = await res.json();
        const lista = document.getElementById("lista-menu");
        lista.innerHTML = "";

        if (!productos || productos.length === 0) {
            lista.innerHTML = `<li class="list-group-item text-muted text-center">No hay productos registrados.</li>`;
            return;
        }

        productos.forEach(p => {
            lista.innerHTML += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${p.nombre}</strong>
                        ${p.descripcion ? `<br><small class="text-muted">${p.descripcion}</small>` : ''}
                    </div>
                    <span class="badge bg-primary rounded-pill">$${p.precio}</span>
                </li>`;
        });
    } catch (err) {
        console.error("Error al obtener el menú:", err);
    }
}

// Cargar Lista de Mesas
async function cargarMesas() {
    try {
        const res = await fetch(`${API_URL}/mesero/tables`);
        const mesas = await res.json();
        const grid = document.getElementById("grid-mesas");
        grid.innerHTML = "";

        if (!mesas || mesas.length === 0) {
            grid.innerHTML = `<div class="col-12 text-muted text-center">No hay mesas configuradas.</div>`;
            return;
        }

        mesas.forEach(m => {
            grid.innerHTML += `
                <div class="col-6">
                    <div class="card text-center p-2 border-success bg-white">
                        <h6 class="fw-bold mb-1">Mesa ${m.numero}</h6>
                        <small class="text-muted">Capacidad: ${m.capacidad} pers.</small>
                    </div>
                </div>`;
        });
    } catch (err) {
        console.error("Error al obtener las mesas:", err);
    }
}

// Registrar Producto nuevo en la BD
async function crearProducto(e) {
    e.preventDefault();
    const nombre = document.getElementById("prod-nombre").value;
    const precio = parseFloat(document.getElementById("prod-precio").value);
    const descripcion = document.getElementById("prod-descripcion").value;
    const catInput = document.getElementById("prod-categoria").value;

    const categoria_id = catInput ? parseInt(catInput) : 1;

    const payload = {
        nombre: nombre,
        precio: precio,
        descripcion: descripcion || "Sin descripción",
        disponibilidad: true,
        categoria_id: categoria_id
    };

    try {
        const res = await fetch(`${API_URL}/admin/products`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            document.getElementById("form-producto").reset();
            cargarMenu();
            alert("¡Producto creado con éxito!");
        } else {
            const errorData = await res.json();
            alert("Error " + res.status + ": " + JSON.stringify(errorData.detail || errorData));
        }
    } catch (err) {
        alert("Error de conexión al guardar el producto.");
    }
}

// Registrar Mesa nueva en la BD
async function crearMesa(e) {
    e.preventDefault();
    const numero = parseInt(document.getElementById("mesa-numero").value);
    const capacidad = parseInt(document.getElementById("mesa-capacidad").value);

    try {
        const res = await fetch(`${API_URL}/admin/tables`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ numero, capacidad })
        });

        if (res.ok) {
            document.getElementById("form-mesa").reset();
            cargarMesas();
            alert("¡Mesa creada con éxito!");
        } else {
            const errorData = await res.json();
            alert("Error al crear la mesa: " + JSON.stringify(errorData.detail || errorData));
        }
    } catch (err) {
        alert("Error de conexión al guardar la mesa.");
    }
}

// Cargar datos al abrir la página
window.onload = () => {
    cargarMenu();
    cargarMesas();
};