"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { TopKClass } from "@/lib/types";

interface ConfidenceChartProps {
  classes: TopKClass[];
}

const BAR_COLORS = [
  "#7c3aed", // brand purple
  "#a574ff",
  "#22d3ee",
  "#34d399",
  "#fbbf24",
];

function CustomTooltip({ active, payload }: any) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="glass rounded-xl px-3 py-2 text-xs">
      <p className="text-white font-semibold">{d.label}</p>
      <p className="text-slate-300">{(d.confidence * 100).toFixed(2)}%</p>
    </div>
  );
}

export function ConfidenceChart({ classes }: ConfidenceChartProps) {
  const data = classes.map((c) => ({
    ...c,
    label: c.label.length > 20 ? c.label.slice(0, 20) + "…" : c.label,
    value: parseFloat((c.confidence * 100).toFixed(2)),
  }));

  return (
    <div className="w-full h-52" id="confidence-chart">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 0, right: 16, left: 0, bottom: 0 }}
        >
          <XAxis
            type="number"
            domain={[0, 100]}
            tick={{ fill: "#64748b", fontSize: 10 }}
            tickLine={false}
            axisLine={false}
            unit="%"
          />
          <YAxis
            type="category"
            dataKey="label"
            width={120}
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip
            content={<CustomTooltip />}
            cursor={{ fill: "rgba(255,255,255,0.03)" }}
          />
          <Bar dataKey="value" radius={[0, 6, 6, 0]} maxBarSize={18}>
            {data.map((_, index) => (
              <Cell key={index} fill={BAR_COLORS[index % BAR_COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
