    Sistema de Citas Médicas

Este proyecto fue desarrollado como parte del curso COMP2052 - Web Development with Server-Side and Microservices en la Universidad Interamericana de Puerto Rico. El objetivo principal fue crear una aplicación web funcional para gestionar citas médicas según el rol de cada usuario (Administrador, Médico o Paciente).

    ¿Qué hace esta app?
	•	Permite que los pacientes agenden sus citas médicas.
	•	Los médicos pueden ver y marcar sus citas como realizadas.
	•	Los administradores tienen acceso completo a todos los usuarios y citas.
	•	Incluye autenticación, validación de datos y control de accesos según roles.

     Tecnologías que usamos
	•	Flask (Python) como framework backend.
	•	MariaDB / MySQL para la base de datos.
	•	Jinja2, HTML, CSS, Bootstrap para el frontend.
	•	Flask-Login para manejo de sesiones.
	•	Flask-WTF para formularios.
	•	REST Client para probar las rutas CRUD con citas médicas.

    Equipo
	•	Mikael Tiba – desarrollo de rutas y pruebas.
	•	Janiel Rodríguez – base de datos, lógica de roles y validaciones.

Ambos trabajamos de forma colaborativa y dividimos el trabajo de manera equitativa.

     Funcionalidades clave
	•	Login y registro seguro con roles.
	•	Dashboard personalizado por tipo de usuario.
	•	Agendamiento, cancelación y realización de citas.
	•	Pruebas REST (.rest) para Create, Read, Update y Delete de citas.
