import { Link } from "react-router-dom";
import { UtensilsCrossed } from "lucide-react";

export default function Navbar() {
  return (
    <div className="sticky top-0 z-50 backdrop-blur border-b border-white/10 bg-slate-950/80">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 text-white font-semibold text-xl">
          <div className="p-2 rounded-2xl bg-emerald-500/20">
            <UtensilsCrossed className="w-5 h-5 text-emerald-400" />
          </div>
          SmartDine AI Pro
        </Link>
        <div className="flex gap-6 text-slate-300 text-sm">
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/admin">Admin</Link>
          <Link to="/auth">Login</Link>
        </div>
      </div>
    </div>
  );
}
