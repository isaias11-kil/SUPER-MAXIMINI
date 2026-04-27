CREATE TABLE usuarios (
    UsuarioID INT IDENTITY(1,1) PRIMARY KEY,
    NombreUsuario VARCHAR(50) NOT NULL UNIQUE,
    Contrasena VARCHAR(255) NOT NULL,
    NombreCompleto VARCHAR(100) NOT NULL,
    Rol VARCHAR(50) NOT NULL,
    Estado BIT DEFAULT 1
);
