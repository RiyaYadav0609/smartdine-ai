/*import { useState } from "react";
import { api } from "../lib/api";

export default function BookingModal({ restaurant, onClose }) {
  const [form, setForm] = useState({ user_email: "", guests: 2, slot: "7:00 PM" });
  const [msg, setMsg] = useState("");

  if (!restaurant) return null;

  const submit = async () => {
    try {
      const res = await api.post("/bookings", {
        ...form,
        restaurant_id: restaurant.id
      });
      setMsg(res.data.message + " for " + res.data.restaurant);
    } catch (e) {
      setMsg(e?.response?.data?.detail || "Booking failed");
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 grid place-items-center p-4 z-50">
      <div className="w-full max-w-lg rounded-3xl bg-slate-900 border border-white/10 p-6 text-white">
        <h2 className="text-2xl font-bold">{restaurant.name}</h2>
        <p className="text-slate-400 mt-1">Reserve your table in seconds</p>

        <div className="grid gap-4 mt-5">
          <input className="rounded-2xl bg-white/5 border border-white/10 p-3" placeholder="Your email"
            value={form.user_email} onChange={e => setForm({ ...form, user_email: e.target.value })} />
          <input type="number" className="rounded-2xl bg-white/5 border border-white/10 p-3" placeholder="Guests"
            value={form.guests} onChange={e => setForm({ ...form, guests: Number(e.target.value) })} />
          <select className="rounded-2xl bg-white/5 border border-white/10 p-3"
            value={form.slot} onChange={e => setForm({ ...form, slot: e.target.value })}>
            <option>7:00 PM</option>
            <option>8:00 PM</option>
            <option>9:00 PM</option>
          </select>
        </div>

        {msg && <div className="mt-4 text-emerald-300 text-sm">{msg}</div>}

        <div className="flex gap-3 mt-6">
          <button onClick={submit} className="flex-1 rounded-2xl bg-emerald-500 text-slate-950 font-semibold py-3">Confirm</button>
          <button onClick={onClose} className="flex-1 rounded-2xl bg-white/10 font-semibold py-3">Close</button>
        </div>
      </div>
    </div>
  );
}*/
/*import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function BookingModal({ restaurant, onClose }) {
  const [form, setForm] = useState({
    user_email: "",
    guests: 2,
    slot: "7:00 PM",
  });
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (restaurant) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [restaurant]);

  if (!restaurant) return null;

  const submit = async () => {
    try {
      const res = await api.post("/bookings", {
        ...form,
        restaurant_id: restaurant.id,
      });
      setMsg(res.data.message + " for " + res.data.restaurant);
    } catch (e) {
      setMsg(e?.response?.data?.detail || "Booking failed");
    }
  };

  return (
    <div className="fixed inset-0 z-[9999] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="w-full max-w-lg rounded-3xl bg-slate-900 border border-white/10 p-6 text-white shadow-2xl">
        <h2 className="text-2xl font-bold break-words">{restaurant.name}</h2>
        <p className="text-slate-400 mt-1">Reserve your table in seconds</p>

        <div className="grid gap-4 mt-5">
          <input
            className="rounded-2xl bg-white/5 border border-white/10 p-3"
            placeholder="Your email"
            value={form.user_email}
            onChange={(e) =>
              setForm({ ...form, user_email: e.target.value })
            }
          />

          <input
            type="number"
            className="rounded-2xl bg-white/5 border border-white/10 p-3"
            placeholder="Guests"
            value={form.guests}
            onChange={(e) =>
              setForm({ ...form, guests: Number(e.target.value) })
            }
          />

          <select
            className="rounded-2xl bg-white/5 border border-white/10 p-3"
            value={form.slot}
            onChange={(e) => setForm({ ...form, slot: e.target.value })}
          >
            <option>7:00 PM</option>
            <option>8:00 PM</option>
            <option>9:00 PM</option>
          </select>
        </div>

        {msg && <div className="mt-4 text-emerald-300 text-sm">{msg}</div>}

        <div className="flex gap-3 mt-6">
          <button
            onClick={submit}
            className="flex-1 rounded-2xl bg-emerald-500 text-slate-950 font-semibold py-3"
          >
            Confirm
          </button>

          <button
            onClick={onClose}
            className="flex-1 rounded-2xl bg-white/10 font-semibold py-3"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}*/
import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function BookingModal({ restaurant, onClose }) {
  const [form, setForm] = useState({
    user_email: "",
    guests: 2,
    slot: "7:00 PM",
  });
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (restaurant) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [restaurant]);

  if (!restaurant) return null;

  const submit = async () => {
    try {
      const res = await api.post("/bookings", {
        ...form,
        restaurant_id: restaurant.id,
      });
      setMsg(res.data.message + " for " + res.data.restaurant);
    } catch (e) {
      setMsg(e?.response?.data?.detail || "Booking failed");
    }
  };

  return (
    <div className="fixed inset-0 z-[9999] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="w-full max-w-lg rounded-3xl bg-slate-900 border border-white/10 p-6 text-white shadow-2xl">
        <h2 className="text-2xl font-bold break-words">{restaurant.name}</h2>
        <p className="text-slate-400 mt-1">Reserve your table in seconds</p>

        <div className="grid gap-4 mt-5">
          <input
            className="rounded-2xl bg-white/5 border border-white/10 p-3 text-white placeholder:text-slate-400"
            placeholder="Your email"
            value={form.user_email}
            onChange={(e) =>
              setForm({ ...form, user_email: e.target.value })
            }
          />

          <input
            type="number"
            min="1"
            className="rounded-2xl bg-white/5 border border-white/10 p-3 text-white"
            placeholder="Guests"
            value={form.guests}
            onChange={(e) =>
              setForm({ ...form, guests: Number(e.target.value) })
            }
          />

          <select
            className="rounded-2xl bg-slate-800 border border-white/10 p-3 text-white"
            value={form.slot}
            onChange={(e) => setForm({ ...form, slot: e.target.value })}
          >
            <option value="8:00 AM">8:00 AM</option>
            <option value="9:00 AM">9:00 AM</option>
            <option value="10:00 AM">10:00 AM</option>
            <option value="11:00 AM">11:00 AM</option>
            <option value="12:00 PM">12:00 PM</option>
            <option value="1:00 PM">1:00 PM</option>
            <option value="2:00 PM">2:00 PM</option>
            <option value="3:00 PM">3:00 PM</option>
            <option value="4:00 PM">4:00 PM</option>
            <option value="5:00 PM">5:00 PM</option>
            <option value="6:00 PM">6:00 PM</option>
            <option value="7:00 PM">7:00 PM</option>
            <option value="8:00 PM">8:00 PM</option>
            <option value="9:00 PM">9:00 PM</option>
            <option value="10:00 PM">10:00 PM</option>
          </select>
        </div>

        {msg && <div className="mt-4 text-emerald-300 text-sm">{msg}</div>}

        <div className="flex gap-3 mt-6">
          <button
            onClick={submit}
            className="flex-1 rounded-2xl bg-emerald-500 text-slate-950 font-semibold py-3"
          >
            Confirm
          </button>

          <button
            onClick={onClose}
            className="flex-1 rounded-2xl bg-white/10 font-semibold py-3"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
