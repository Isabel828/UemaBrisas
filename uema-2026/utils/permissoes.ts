export function isAdmin(user: any): boolean {
  if (!user) return false;

  return (
    user?.username === "admin" ||   // 👈 garante que funcione agora
    user?.is_staff === true ||
    user?.is_superuser === true ||
    user?.role === "admin" ||
    user?.tipo === "admin" ||
    user?.perfil === "admin"
  );
}