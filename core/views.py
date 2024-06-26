from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, mascotas_salvadas, Boleta
from .forms import RegistroUserForm, FormProducto, Form_Mascotas_Salvadas
from core.compras import Carrito
from decimal import Decimal

# Vistas principales
def Home(request):
    return render(request, 'Home.html')

def productos(request):
    categorias = Categoria.objects.all()

    productos_por_categoria = {}
    for categoria in categorias:
        productos_por_categoria[categoria.nombre] = Producto.objects.filter(categoria=categoria)

    context = {
        'productos_por_categoria': productos_por_categoria,
    }

    return render(request, 'productos.html', context)

def Acercade(request):
    return render(request, 'Acerca_de.html')

def Mascotas(request):
    mascotas = mascotas_salvadas.objects.all()
    return render(request, 'Mascotas.html', {'mascotas': mascotas})

def carrito(request):
    return render(request, 'carrito.html')

def cerrar(request):
    logout(request)
    return redirect('Home')

def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'tienda.html', {'productos': productos})

def registrar(request):
    data = {'form': RegistroUserForm()}
    if request.method == "POST":
        formulario = RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],
                                password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect('Home')
        data["form"] = formulario
    return render(request, 'registration/registrar.html', data)

# Creación y edición de productos
def crear_producto(request):
    if request.method == 'POST':
        form = FormProducto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Asegúrate de que 'lista_productos' sea una URL válida.
    else:
        form = FormProducto()
    
    return render(request, 'crear_producto.html', {'form': form})


def eliminar_producto_admin(request, id):
    producto = get_object_or_404(Producto, idProd=id)
    
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')  # Redirige a la lista de productos después de eliminar
    
    return render(request, 'eliminar.html', {'producto': producto})


def modificar_producto(request, id):
    producto = get_object_or_404(Producto, idProd=id)
    
    if request.method == 'POST':
        form = FormProducto(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a la lista de productos después de modificar
    else:
        form = FormProducto(instance=producto)
    
    return render(request, 'modificar.html', {'form': form, 'producto': producto})

# Listas y detalles de productos
def lista_productos(request):
    categorias = Categoria.objects.all()

    productos_por_categoria = {}
    for categoria in categorias:
        productos_por_categoria[categoria.nombre] = Producto.objects.filter(categoria=categoria)

    context = {
        'productos_por_categoria': productos_por_categoria,
    }

    return render(request, 'productos.html', context)


def lista_mascotas_salvadas(request):
    mascotas = mascotas_salvadas.objects.all()
    return render(request, 'productos.html', {'productos': mascotas, 'tipo': 'mascotas_salvadas'})

# Carrito de compras y boleta
def agregar_producto(request, id):
    producto = get_object_or_404(Producto, idProd=id)
    carrito = Carrito(request)
    carrito.agregar_producto(producto)
    return redirect('tienda')


def limpiar_carrito(request):
    carrito_compra = Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')


def restar_producto_carrito(request, id):
    producto = Producto.objects.get(idProd=id)
    carrito = Carrito(request)
    carrito.restar_producto(producto)
    return redirect('tienda')

def agregar_producto_carrito(request, id):
    producto = Producto.objects.get(idProd=id)
    carrito = Carrito(request)
    carrito.agregar_producto(producto)
    return redirect('tienda')

def eliminar_producto_carrito(request, id):
    producto = Producto.objects.get(idProd=id)
    carrito = Carrito(request)
    carrito.eliminar_producto(producto)
    return redirect('tienda')

def generar_boleta(request):
    carrito = request.session.get('carrito', {})
    total = 0
    
    for key, value in carrito.items():

        producto = Producto.objects.get(idProd=key)
 
        subtotal = producto.precio * value['cantidad']
        total += subtotal
        producto.stock -= value['cantidad']
        producto.save()
        
        value['subtotal'] = subtotal

    request.session['carrito'] = {}
    
    context = {
        'carrito': carrito,
        'total': total,
    }
    
    return render(request, 'boleta.html', context)
