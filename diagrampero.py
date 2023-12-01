from diagrams import Diagram, Cluster
from diagrams.aws.general import (
    User, InternetAlt2, TraditionalServer, SslPadlock, GenericFirewall,MobileClient, InternetGateway, Client
)
from diagrams.aws.migration import TransferForSftp
from diagrams.aws.network import ALB, PrivateSubnet, PublicSubnet, VPC, VpnConnection
from diagrams.aws.compute import EC2Instances, EC2
from diagrams.aws.security import Inspector, KMS, IdentityAndAccessManagementIamAddOn,WAF
from diagrams.aws.database import DB, RDSSqlServerInstance, RDSPostgresqlInstance, RDSMariadbInstance,RDS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SQS

from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.analytics import Hadoop
from diagrams.onprem.logging import Loki
from diagrams.onprem.iac import Terraform

from diagrams.generic.network import Router, Switch, Firewall
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage
from diagrams.generic.database import SQL
from diagrams.generic.os import Windows, Ubuntu


def clasificar_por_secciones(lista):
    secciones = {
        'usuarios': ['User', 'InternetAlt2', 'TraditionalServer'],
        'conexion': ['WAF', 'SslPadlock', 'GenericFirewall', 'TransferForSftp'],
        'servicio': ['ALB', 'EC2Instances', 'EC2'],
        'seguridad': ['Inspector', 'KMS', 'IdentityAndAccessManagementIamAddOn'],
        'base_de_datos': ['DB', 'RDSSqlServerInstance', 'RDSPostgresqlInstance', 'RDSMariadbInstance'],
        'ejemplos':['DiagramaCloud','DiagramaRed','DiagramaRedInterna','DiagramaRedEmpresa']
    }

    resultado = {seccion: [] for seccion in secciones}

    for elemento in lista:
        for seccion, palabras_clave in secciones.items():
            if any(palabra_clave_elemento.lower() in elemento.lower() for palabra_clave_elemento in palabras_clave):
                resultado[seccion].append(elemento)
                break

    return resultado


def generar_diagrama(secciones):
    usuarios_elements = []
    conexion_elements = []
    servicio_elements = []
    seguridad_elements = []
    base_de_datos_elements = []

    if 'ejemplos' in secciones and secciones['ejemplos']:
        for elemento in secciones['ejemplos']:
            if elemento == 'DiagramaCloud':
                # Lógica específica para DiagramaCloud
                print("Generando DiagramaCloud...")
                with Diagram("Arquitectura", show=False):
                    with Cluster("Actors"):
                        user = User("User")
                        internet = InternetAlt2("Internet")
                        server0 = TraditionalServer("Server")

                    with Cluster("Conection"):
                        seg = [WAF("Waf")
                        ,SslPadlock("Peticiones")
                        ,GenericFirewall("FireWall")
                        ,TransferForSftp("SFTP")]

                    with Cluster("Cloud"):
                        alb = ALB("Valanceador de Carga")

                        with Cluster("Public Subnet"):
                            server1 = EC2Instances("Server 1")
                            server2 = EC2Instances("Server 2")
                            server3 = EC2("")

                    with Cluster("Segurity Manager"):
                        security = Inspector("Inspector")
                        kms = KMS("KMS")
                        id = IdentityAndAccessManagementIamAddOn("IAM")

                    with Cluster("Database Manager"):
                        database =[ DB("DataBase")
                        ,RDSSqlServerInstance("") 
                        ,RDSPostgresqlInstance("") 
                        ,RDSMariadbInstance("")]

                    user >> internet
                    internet >> seg
                    seg >> alb
                    alb >> server2
                    server2 >> kms
                    kms >> database

            elif elemento == 'DiagramaRed':
                # Lógica específica para DiagramaRed
                print("Generando DiagramaRed...")
                with Diagram("Arquitectura", show=False):
                    internet_gateway = InternetGateway("Internet Gateway")

                    with Cluster("Red Privada"):
                        vpc = VPC("VPC")
                        private_subnet1 = PrivateSubnet("Private Subnet 1")
                        private_subnet2 = PrivateSubnet("Private Subnet 2")
                        ec2_instance = EC2("EC2 Instance")
                        rds_instance = RDS("RDS Instance")

                    with Cluster("Red Pública"):
                        public_subnet = PublicSubnet("Public Subnet")
                        load_balancer = SQS("Load Balancer")

                    mobile_client = MobileClient("Mobile Client")
                    client = Client("Client")

                    # Conexiones
                    internet_gateway >> public_subnet
                    mobile_client >> public_subnet
                    client >> private_subnet1
                    client >> private_subnet2

                    ec2_instance >> private_subnet1
                    rds_instance >> private_subnet2

                    # Otros elementos
                    vpc >> [public_subnet, private_subnet1, private_subnet2]
                    internet_gateway >> vpc
                    load_balancer >> [ec2_instance, rds_instance]

                    # Servicios de monitoreo
                    cloudwatch = Cloudwatch("CloudWatch")
                    cloudwatch >> [ec2_instance, rds_instance]

                    # VPN Connection
                    vpn_connection = VpnConnection("VPN Connection")
                    vpn_connection >> vpc

                
            elif elemento == 'DiagramaRedInterna':
                # Lógica específica para DiagramaRedInterna
                print("Generando DiagramaRedInterna...")
                with Diagram("Arquitectura", show=False):
                    internet = Internet("internet")

                    with Cluster("Centro de Datos"):
                        # Servidores Web
                        with Cluster("Capa de Aplicación"):
                            app_servers = [Server("App Server 1"), Server("App Server 2")]

                        # Base de Datos
                        with Cluster("Capa de Base de Datos"):
                            db_master = PostgreSQL("DB Master")
                            db_master - PostgreSQL("DB Slave")

                        # Cache
                        with Cluster("Capa de Caché"):
                            cache = Redis("Redis Cache")

                        # Logs y Monitoreo
                        with Cluster("Capa de Monitoreo y Logs"):
                            monitoring = Grafana("Monitoring")
                            logs = Loki("Logs")

                        # Agregación de Logs
                        with Cluster("Capa de Agregación de Logs"):
                            aggregator = Fluentd("Log Aggregator")
                            aggregator >> Hadoop("Data Lake")

                        # Infraestructura como Código
                        with Cluster("Gestión de Infraestructura"):
                            iac = Terraform("Terraform")

                        # Conexiones
                        internet >> app_servers >> db_master
                        internet >> app_servers >> cache
                        app_servers >> monitoring
                        app_servers >> logs
                        app_servers >> aggregator
                        iac >> app_servers
                        iac >> db_master
                        iac >> cache
                        iac >> monitoring
                        iac >> logs
                        iac >> aggregator
            elif elemento == 'DiagramaRedEmpresa':
                # Lógica específica para DiagramaRedEmpresa
                print("Generando DiagramaRedEmpresa...")
                with Diagram("Arquitectura", show=False):
                    internet = Internet("Internet")
                    gateway = Router("Gateway")
                    firewall = Firewall("Firewall")
                    honeypot = Ubuntu("Honeypot")
                    sandbox = Storage("Sandbox")

                    with Cluster("Subred Pública"):
                        switch_public = Switch("Switch")
                        public_servers = [Storage("Server 1"), Storage("Server 2")]

                    with Cluster("Subred Privada"):
                        switch_private = Switch("Switch")
                        private_servers = [Storage("Server 3"),Storage("Server 4")]

                    with Cluster("VLANs"):
                        vlan_switch = Switch("Switch VLAN")
                        vlans = [Rack("VLAN 1"), Rack("VLAN 2")]

                    with Cluster("Base de Datos"):
                        db = SQL("Base de Datos")

                    with Cluster("PCs"):
                        pcs = [Windows("PC 1"), Windows("PC 2")]

                    # Conexiones
                    internet >> gateway >> firewall >> switch_public
                    firewall >> honeypot
                    firewall >> sandbox
                    switch_public >> public_servers
                    switch_public >> switch_private >> private_servers
                    switch_private >> vlan_switch >> vlans
                    switch_private >> db
                    switch_private >> pcs

            else:
                print(f"Elemento no reconocido:")   
    else:
        print("La sección 'ejemplos' no está presente en las secciones o está vacía.")

        with Diagram("Arquitectura", show=False):
            if 'usuarios' in secciones and secciones['usuarios']:
                with Cluster("Usuarios"):
                    for elemento in secciones['usuarios']:
                        instance = eval(elemento)()
                        usuarios_elements.append(instance)

            if 'conexion' in secciones and secciones['conexion']:
                with Cluster("Conexión"):
                    for elemento in secciones['conexion']:
                        instance = eval(elemento)()
                        conexion_elements.append(instance)

            if 'servicio' in secciones and secciones['servicio']:
                with Cluster("Servicio"):
                    for elemento in secciones['servicio']:
                        instance = eval(elemento)()
                        servicio_elements.append(instance)

            if 'seguridad' in secciones and secciones['seguridad']:
                with Cluster("Seguridad"):
                    for elemento in secciones['seguridad']:
                        instance = eval(elemento)()
                        seguridad_elements.append(instance)

            if 'base_de_datos' in secciones and secciones['base_de_datos']:
                with Cluster("Base de Datos"):
                    for elemento in secciones['base_de_datos']:
                        instance = eval(elemento)()
                        base_de_datos_elements.append(instance)

            # Realizar conexiones según la lógica especificada
            if usuarios_elements:
                if conexion_elements:
                    usuarios_elements[0] >> conexion_elements[0]
                elif servicio_elements:
                    usuarios_elements[0] >> servicio_elements[0]
                elif seguridad_elements:
                    usuarios_elements[0] >> seguridad_elements[0]
                elif base_de_datos_elements:
                    usuarios_elements[0] >> base_de_datos_elements[0]

            if conexion_elements:
                if servicio_elements:
                    conexion_elements[0] >> servicio_elements[0]
                elif seguridad_elements:
                    conexion_elements[0] >> seguridad_elements[0]
                elif base_de_datos_elements:
                    conexion_elements[0] >> base_de_datos_elements[0]

            if servicio_elements:
                if seguridad_elements:
                    servicio_elements[0] >> seguridad_elements[0]
                elif base_de_datos_elements:
                    servicio_elements[0] >> base_de_datos_elements[0]

            if seguridad_elements and base_de_datos_elements:
                seguridad_elements[0] >> base_de_datos_elements[0]

# Ejemplo de uso
#secciones = { 'conexion': ['WAF', 'GenericFirewall'], 'servicio': ['EC2'],  'base_de_datos': ['DB','RDSSqlServerInstance', 'RDSPostgresqlInstance', 'RDSMariadbInstance']}
#generar_diagrama(secciones)

