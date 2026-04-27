CREATE DATABASE SuperMaximiniDB;
GO

USE SuperMaximiniDB;
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Usuarios' and xtype='U')
BEGIN
    CREATE TABLE Usuarios (
        UsuarioID INT IDENTITY(1,1) PRIMARY KEY,
        NombreCompleto NVARCHAR(100) NOT NULL,
        Username NVARCHAR(50) NOT NULL UNIQUE,
        PasswordHash NVARCHAR(255) NOT NULL,
        Rol NVARCHAR(20) NOT NULL DEFAULT 'Cajero' -- Roles: 'Admin', 'Cajero'
    );
END
GO

-- Insert default admin user if it doesn't exist
-- Note: In a real environment, PasswordHash should be hashed with bcrypt.
-- For development/testing fallback as per instructions, using plaintext or known hash placeholder if acceptable.
-- Since memory says "authentication logic currently includes a fallback to support plaintext passwords for testing",
-- we will just insert the plaintext password here.
IF NOT EXISTS (SELECT * FROM Usuarios WHERE Username = 'admin')
BEGIN
    INSERT INTO Usuarios (NombreCompleto, Username, PasswordHash, Rol)
    VALUES ('Administrador', 'admin', 'admin123', 'Admin');
END
GO
