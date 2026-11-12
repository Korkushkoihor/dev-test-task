import { createFileRoute, redirect } from "@tanstack/react-router"

import { UsersService } from "@/client"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/metrics")({
  component: Metrics,
  beforeLoad: async () => {
    const { data: user } = await UsersService.readUserMe()
    if (user.role !== "admin" && user.role !== "manager" && !user.is_superuser) {
      throw redirect({ to: "/" })
    }
  },
})

function Metrics() {
  const { user } = useAuth()
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold tracking-tight">Metrics</h1>
      <p className="text-muted-foreground">Usage metrics are available to managers and administrators.</p>
      <div className="rounded-lg border p-6">Role: {user?.role ?? (user?.is_superuser ? "admin" : "member")}</div>
    </div>
  )
}
