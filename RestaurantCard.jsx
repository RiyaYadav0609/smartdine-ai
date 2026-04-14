/*export default function RestaurantCard({ item, onBook }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-white/10 to-white/5 p-5 text-white shadow-xl">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-xl font-bold">{item.name}</h3>
          <p className="text-slate-300">{item.city}, {item.state} • {item.cuisine}</p>
        </div>
        <div className="text-right">
          <div className="text-amber-300 font-semibold">⭐ {item.rating}</div>
          <div className="text-xs text-slate-400">Smart score: {item.smart_score}</div>
          <div className="text-[11px] text-emerald-300 mt-1">
            {item.analysis_source === "cv_video_analysis" ? "CV-based" : "Default data"}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-5">
        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Crowd</div>
          <div className="font-semibold">{item.crowd_count}</div>
        </div>
        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Wait</div>
          <div className="font-semibold">{item.waiting_time} min</div>
        </div>
        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Distance</div>
          <div className="font-semibold">{item.distance_km} km</div>
        </div>
        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Tables</div>
          <div className="font-semibold">
            {item.occupied_tables != null ? `${item.occupied_tables}/${(item.occupied_tables || 0) + (item.free_tables || 0)}` : "NA"}
          </div>
        </div>
      </div>

      <div className="mt-5">
        <div className="text-sm text-slate-300 mb-2">Feature impact</div>
        <div className="flex flex-wrap gap-2">
          {Object.entries(item.feature_impact).map(([k, v]) => (
            <span key={k} className="rounded-full px-3 py-1 bg-emerald-500/15 text-emerald-300 text-xs">
              {k}: {v}
            </span>
          ))}
        </div>
      </div>

      <button
        onClick={() => onBook(item)}
        className="mt-5 w-full rounded-2xl bg-emerald-500 hover:bg-emerald-400 transition px-4 py-3 font-semibold text-slate-950"
      >
        Book Table
      </button>
    </div>
  );
}*/
export default function RestaurantCard({ item, onBook }) {
  const sourceLabel =
    item.data_source === "cv"
      ? "CV-based"
      : item.data_source === "real"
      ? "Real Nearby"
      : "Default";

  return (
    <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-white/10 to-white/5 p-5 text-white shadow-xl relative">
      <div className="flex items-start justify-between gap-4 pr-24">
        <div className="min-w-0">
          <h3 className="text-xl font-bold break-words">{item.name}</h3>
          <p className="text-slate-300 break-words">
            {item.city}, {item.state} • {item.cuisine}
          </p>
        </div>

        <div className="text-right shrink-0">
          <div className="text-amber-300 font-semibold">⭐ {item.rating}</div>
          <div className="text-xs text-slate-400">
            Smart score: {item.smart_score}
          </div>
        </div>
      </div>

      <div className="absolute top-4 right-4 rounded-full px-3 py-1 text-xs font-semibold bg-black/70 border border-white/10">
        {sourceLabel}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-5">
        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Crowd</div>
          <div className="font-semibold">{item.crowd_count}</div>
        </div>

        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Wait</div>
          <div className="font-semibold">{item.waiting_time} min</div>
        </div>

        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Distance</div>
          <div className="font-semibold">{item.distance_km} km</div>
        </div>

        <div className="rounded-2xl bg-black/20 p-3">
          <div className="text-slate-400 text-xs">Tables</div>
          <div className="font-semibold">
            {item.free_tables !== null && item.free_tables !== undefined
              ? item.free_tables
              : "NA"}
          </div>
        </div>
      </div>

      <div className="mt-5">
        <div className="text-sm text-slate-300 mb-2">Feature impact</div>
        <div className="flex flex-wrap gap-2">
          {Object.entries(item.feature_impact || {}).map(([k, v]) => (
            <span
              key={k}
              className="rounded-full px-3 py-1 bg-emerald-500/15 text-emerald-300 text-xs"
            >
              {k}: {v}
            </span>
          ))}
        </div>
      </div>

      <button
        onClick={() => onBook(item)}
        className="mt-5 w-full rounded-2xl bg-emerald-500 hover:bg-emerald-400 transition px-4 py-3 font-semibold text-slate-950"
      >
        Book Table
      </button>
    </div>
  );
}
