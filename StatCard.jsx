export default function StatCard({ title, value, subtitle }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-5 shadow-xl">
      <div className="text-slate-400 text-sm">{title}</div>
      <div className="text-3xl font-bold text-white mt-2">{value}</div>
      <div className="text-slate-500 text-sm mt-1">{subtitle}</div>
    </div>
  );
}
