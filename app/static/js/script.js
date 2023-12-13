document.addEventListener('DOMContentLoaded', function () {
    let carrito = [];
    const contenedorCompra = document.getElementById('contenedorCompra');
    const iconoCarrito = document.querySelector('.carrito');
    const xCerrar = document.getElementById('contenedorCompra').querySelector('#x');
    const productosCompra = document.getElementById('productosCompra');
    const total = document.getElementById('total');
    const numeroCarrito = document.querySelector('.numero');

    function agregarAlCarrito(nombre, precio) {
        const productoExistente = carrito.find(producto => producto.nombre === nombre);

        if (productoExistente) {
            productoExistente.cantidad++;
        } else {
            const producto = { nombre, precio, cantidad: 1 };
            carrito.push(producto);
        }

        actualizarCarrito();
    }

    function eliminarDelCarrito(nombre) {
        carrito = carrito.filter(producto => producto.nombre !== nombre);
        actualizarCarrito();
    }

    function actualizarCarrito() {
        productosCompra.innerHTML = '';

        carrito.forEach(producto => {
            const productoDiv = document.createElement('div');
            productoDiv.innerHTML = `${producto.nombre} - $${producto.precio} x ${producto.cantidad}
                <button class="mas">+</button>
                <button class="menos">-</button>
                <button class="eliminar"><img src="static/imagenes/trash.png" alt="Eliminar"></button>`;

            productosCompra.appendChild(productoDiv);

            const botonMas = productoDiv.querySelector('.mas');
            const botonMenos = productoDiv.querySelector('.menos');
            const botonEliminar = productoDiv.querySelector('.eliminar');

            botonMas.addEventListener('click', () => {
                agregarAlCarrito(producto.nombre, producto.precio);
            });

            botonMenos.addEventListener('click', () => {
                eliminarDelCarrito(producto.nombre);
            });

            botonEliminar.addEventListener('click', () => {
                eliminarDelCarrito(producto.nombre);
            });
        });

        const totalCarrito = carrito.reduce((total, producto) => total + producto.precio * producto.cantidad, 0);
        total.textContent = `Total: $${totalCarrito}`;
        numeroCarrito.textContent = carrito.reduce((total, producto) => total + producto.cantidad, 0);
    }

    iconoCarrito.addEventListener('click', () => {
        contenedorCompra.classList.toggle('mostrar');
    });

    xCerrar.addEventListener('click', () => {
        contenedorCompra.classList.remove('mostrar');
    });

    const botonesAgregarCarrito = document.querySelectorAll('.agregar-carrito');

    botonesAgregarCarrito.forEach(boton => {
        boton.addEventListener('click', () => {
            const nombre = boton.parentElement.querySelector('p').textContent;
            const precio = parseFloat(boton.parentElement.querySelector('p:nth-child(3)').textContent.slice(1));
            agregarAlCarrito(nombre, precio);
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const formInicioSesion = document.getElementById('form-inicio-sesion');

    formInicioSesion.addEventListener('submit', function (event) {
        event.preventDefault();

        // Obtener los datos del formulario
        const nombreUsuario = document.getElementById('nombre-usuario').value;
        const contrasena = document.getElementById('contrasena').value;

        // Realizar una solicitud al servidor para el inicio de sesión
        // Puedes usar Fetch o cualquier otra biblioteca para hacer solicitudes HTTP
        // Ejemplo usando Fetch:
        fetch('/inicio-sesion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nombreUsuario: nombreUsuario,
                contrasena: contrasena,
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Manejar la respuesta del servidor
            console.log(data);
            // Puedes redirigir a otra página, mostrar mensajes de éxito/error, etc.
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    });
});
