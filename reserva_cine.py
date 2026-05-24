# ==============================================================================
# ESTRUCTURAS DE DATOS GLOBALES
# ==============================================================================

# Clientes se guardarán como: { "12345678-9": {"nombre": "Juan", "tel": "91234...", "mail": "...", "vigencia": "S"} }
clientes = {}

# Reservas se guardarán como: { "12345678-9": [asiento1, asiento2, ...] }
reservas = {}

# Sala de cine: Matriz de 5x8 (Lista de listas con números del 1 al 40)
sala_cine = [
    [1, 2, 3, 4, 5, 6, 7, 8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40]
]

# ==============================================================================
# MENÚ PRINCIPAL Y FLUJO
# ==============================================================================
# ==============================================================================
# GESTIÓN DE CLIENTES (CRUD)
# ==============================================================================

def crear_cliente():
    print("\n--- CREAR NUEVO CLIENTE ---")
    rut = input("Ingrese RUT (con guión y dígito verificador, ej: 12345678-9): ").strip()
    
    # Regla: No se debe permitir registrar dos clientes con el mismo RUT
    if rut in clientes:
        print("[ERROR] Ya existe un cliente registrado con ese RUT.")
        return

    nombre = input("Ingrese Nombre completo: ").strip()
    telefono = input("Ingrese Teléfono: ").strip()
    mail = input("Ingrese E-mail: ").strip()
    
    # Validación de vigencia (S o N)
    while True:
        vigencia = input("¿Cliente vigente? (S/N): ").strip().upper()
        if vigencia in ["S", "N"]:
            break
        print("[ERROR] Por favor, ingrese solo 'S' para Sí o 'N' para No.")

    # Guardar en nuestro diccionario global
    clientes[rut] = {
        "nombre": nombre,
        "telefono": telefono,
        "mail": mail,
        "vigencia": vigencia
    }
    print(f"\n[ÉXITO] Cliente {nombre} registrado correctamente.")


def listar_clientes():
    print("\n--- LISTA DE CLIENTES REGISTRADOS ---")
    
    # Si el diccionario está vacío
    if not clientes:
        print("No hay clientes registrados en el sistema.")
        return
    
    # Mostrar datos principales de cada cliente
    for rut, datos in clientes.items():
        print(f"RUT: {rut} | Nombre: {datos['nombre']} | Teléfono: {datos['telefono']} | Mail: {datos['mail']} | Vigente: {datos['vigencia']}")
def modificar_cliente():
    print("\n--- MODIFICAR DATOS DE CLIENTE ---")
    rut = input("Ingrese el RUT del cliente que desea modificar: ").strip()
    
    # Verificar si el cliente existe
    if rut not in clientes:
        print("[ERROR] El cliente con ese RUT no está registrado.")
        return
    
    print(f"\nModificando al cliente: {clientes[rut]['nombre']}")
    print("(Deje en blanco y presione Enter si no desea cambiar el campo)")
    
    nuevo_nombre = input(f"Nuevo Nombre [{clientes[rut]['nombre']}]: ").strip()
    nuevo_tel = input(f"Nuevo Teléfono [{clientes[rut]['telefono']}]: ").strip()
    nuevo_mail = input(f"Nuevo E-mail [{clientes[rut]['mail']}]: ").strip()
    
    # Si ingresó datos, los actualizamos; si no, se quedan los anteriores
    if nuevo_nombre:
        clientes[rut]['nombre'] = nuevo_nombre
    if nuevo_tel:
        clientes[rut]['telefono'] = nuevo_tel
    if nuevo_mail:
        clientes[rut]['mail'] = nuevo_mail
        
    # Modificar vigencia con validación
    while True:
        nueva_vigencia = input(f"¿Nueva Vigencia? S/N [{clientes[rut]['vigencia']}]: ").strip().upper()
        if not nueva_vigencia:  # Si presiona enter sin escribir nada
            break
        if nueva_vigencia in ["S", "N"]:
            clientes[rut]['vigencia'] = nueva_vigencia
            break
        print("[ERROR] Ingrese 'S' para Sí o 'N' para No.")
        
    print(f"\n[ÉXITO] Datos de cliente con RUT {rut} actualizados.")


def eliminar_cliente():
    print("\n--- ELIMINAR CLIENTE ---")
    rut = input("Ingrese el RUT del cliente que desea eliminar: ").strip()
    
    # Verificar si el cliente existe
    if rut not in clientes:
        print("[ERROR] El cliente con ese RUT no está registrado.")
        return
    
    nombre_cliente = clientes[rut]['nombre']
    
    # Eliminar al cliente del diccionario de clientes [cite: 29]
    del clientes[rut]
    
    # REGLA: Al eliminar un cliente, también se debe eliminar cualquier reserva asociada a ese RUT [cite: 30]
    if rut in reservas:
        del reservas[rut]
        print(f"[AVISO] Se eliminaron las reservas asociadas al RUT {rut}.")
        
    print(f"\n[ÉXITO] El cliente {nombre_cliente} ha sido eliminado del sistema.")

def imprimir_sala():
    print("\n" + "-" * 15 + " Sala de Cine " + "-" * 15)
    
    # Recorremos cada fila de nuestra matriz de la sala [cite: 52]
    for fila in sala_cine:
        linea_asientos = ""
        
        for asiento in fila:
            # Revisamos si este número de asiento está en las reservas de algún cliente
            asiento_ocupado = False
            for asientos_cliente in reservas.values():
                if asiento in asientos_cliente:
                    asiento_ocupado = True
                    break
            
            # Si está ocupado imprimimos [XX], si no, su número [cite: 55, 57]
            if asiento_ocupado:
                linea_asientos += " [XX]"
            else:
                linea_asientos += f" [{format(asiento, '02d')}]"
                
        print(linea_asientos)
        
    print("\n XX = Asiento reservado")
def reservar_asientos():
    print("\n--- RESERVAR ASIENTOS ---")
    rut = input("Ingrese el RUT del cliente que realiza la reserva: ").strip()
    
    # Regla: El cliente debe estar previamente registrado
    if rut not in clientes:
        print("[ERROR] El cliente no está registrado en el sistema. Debe crearlo primero.")
        return
        
    # Regla: El cliente debe estar vigente
    if clientes[rut]["vigencia"] == "N":
        print("[ERROR] El cliente no está vigente. No puede realizar reservas.")
        return

    # Mostrar la sala para que el cliente vea qué asientos están libres
    imprimir_sala()
    
    # Solicitar cuántos asientos desea reservar
    try:
        cantidad = int(input("\n¿Cuántos asientos desea reservar?: "))
        if cantidad <= 0:
            print("[ERROR] La cantidad debe ser mayor a 0.")
            return
    except ValueError:
        print("[ERROR] Debe ingresar un número entero válido.")
        return

    nuevos_asientos = []
    
    # Iterar para pedir cada asiento
    for i in range(cantidad):
        try:
            asiento = int(input(f"Ingrese el número del asiento {i+1} (1-40): "))
            
            # Regla: El asiento seleccionado debe existir
            if asiento < 1 or asiento > 40:
                print(f"[ERROR] El asiento {asiento} no existe en la sala. Reserva cancelada.")
                return
                
            # Regla: El asiento no debe estar reservado por otro cliente (ni por él mismo en este proceso)
            asiento_ocupado = False
            for asientos_cliente in reservas.values():
                if asiento in asientos_cliente:
                    asiento_ocupado = True
                    break
            
            if asiento_ocupado or (asiento in nuevos_asientos):
                print(f"[ERROR] El asiento {asiento} ya está reservado u ocupado en esta selección. Reserva cancelada.")
                return
                
            nuevos_asientos.append(asiento)
            
        except ValueError:
            print("[ERROR] Entrada inválida. Debe ingresar números de asiento. Reserva cancelada.")
            return

    # Regla: Guardar la reserva asociada al RUT del cliente
    # Si el cliente ya tenía asientos reservados, se los sumamos; si no, creamos la lista
    if rut in reservas:
        reservas[rut].extend(nuevos_asientos)
    else:
        reservas[rut] = nuevos_asientos

    print(f"\n[ÉXITO] Se han reservado los asientos {nuevos_asientos} para el cliente {clientes[rut]['nombre']}.")
def modificar_reserva():
    print("\n--- MODIFICAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para modificar su reserva: ").strip()
    
    # Regla: Verificar si el cliente tiene una reserva registrada
    if rut not in reservas:
        print("[ERROR] No se encontraron reservas asociadas a este RUT.")
        return
        
    print(f"\nCliente: {clientes[rut]['nombre']}")
    print(f"Reserva actual: Asientos {reservas[rut]}")
    
    # Mostrar la sala actual para referencia
    imprimir_sala()
    
    print("\nAl modificar, ingresará una nueva lista de asientos desde cero.")
    print("Si desea conservar alguno de sus asientos anteriores, debe volver a ingresarlo.")
    
    try:
        cantidad = int(input("¿Cuántos asientos tendrá su nueva reserva?: "))
        if cantidad <= 0:
            print("[ERROR] La cantidad debe ser mayor a 0.")
            return
    except ValueError:
        print("[ERROR] Debe ingresar un número entero válido.")
        return

    nuevos_asientos = []
    
    for i in range(cantidad):
        try:
            asiento = int(input(f"Ingrese el número del asiento {i+1} (1-40): "))
            
            # Regla: El asiento debe existir
            if asiento < 1 or asiento > 40:
                print(f"[ERROR] El asiento {asiento} no existe. Proceso cancelado.")
                return
                
            # Regla: No se pueden ocupar asientos de OTROS clientes.
            # Pero SÍ puede incluir asientos que ya eran de él (según el enunciado).
            asiento_ocupado_por_otro = False
            for otro_rut, asientos_cliente in reservas.items():
                if otro_rut != rut and asiento in asientos_cliente:
                    asiento_ocupado_por_otro = True
                    break
                    
            if asiento_ocupado_por_otro or (asiento in nuevos_asientos):
                print(f"[ERROR] El asiento {asiento} está ocupado por otro cliente o ya lo seleccionó. Proceso cancelado.")
                return
                
            nuevos_asientos.append(asiento)
            
        except ValueError:
            print("[ERROR] Entrada inválida. Proceso cancelado.")
            return

    # Actualizar la lista de asientos del cliente
    reservas[rut] = nuevos_asientos
    print(f"\n[ÉXITO] Reserva modificada. Nuevos asientos del cliente: {reservas[rut]}")


def eliminar_reserva():
    print("\n--- ELIMINAR RESERVA ---")
    rut = input("Ingrese el RUT del cliente para eliminar su reserva: ").strip()
    
    # Regla: Verificar si existe la reserva
    if rut not in reservas:
        print("[ERROR] No existe ninguna reserva asociada a ese RUT.")
        return
        
    # Eliminar la reserva del diccionario (los asientos vuelven a quedar libres automáticamente)
    del reservas[rut]
    print(f"\n[ÉXITO] La reserva ha sido eliminada. Los asientos vuelven a estar disponibles.")


def listar_reservas():
    print("\n--- LISTA DE RESERVAS EXISTENTES ---")
    
    if not reservas:
        print("No hay reservas registradas en el sistema.")
        return
        
    # Regla: Mostrar todas las reservas indicando RUT, Nombre del cliente y Asientos
    for rut, asientos in reservas.items():
        nombre_cliente = clientes[rut]['nombre']
        print(f"RUT: {rut} | Cliente: {nombre_cliente} | Asientos Reservados: {asientos}")
def menu_principal():
    while True:
        print("\n" + "="*36)
        print("   SISTEMA DE RESERVA DE CINE  ")
        print("="*36)
        print("1. Crear cliente")
        print("2. Listar clientes")
        print("3. Modificar cliente")
        print("4. Eliminar cliente")
        print("5. Reservar asientos")
        print("6. Modificar reserva")
        print("7. Eliminar reserva")
        print("8. Listar reservas")
        print("9. Imprimir sala")
        print("10. Salir")
        print("="*36)
        
        opcion = input("Seleccione una opción (1-10): ").strip()
        
        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            modificar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            reservar_asientos()
        elif opcion == "6":
            modificar_reserva()
        elif opcion == "7":
            eliminar_reserva()
        elif opcion == "8":
           listar_reservas()
        elif opcion == "9":
            imprimir_sala()
        elif opcion == "10":
            print("\n¡Gracias por utilizar el sistema! Saliendo...")
            break
        else:
            print("\n[ERROR] Opción no válida. Intente nuevamente.")

# Iniciar el programa
if __name__ == "__main__":
    menu_principal()