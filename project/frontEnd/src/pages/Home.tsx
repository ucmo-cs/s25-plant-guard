import { useEffect, useState } from "react";
import { getCurrentPiData, fetchPiHistory } from "../services/piDataApi";
import { PiData } from "../model/PiData";
import { Card } from "flowbite-react";
import LineChart from "../components/charts/LineChart";

type PiResult = PiData | { pieId: string; error: true };

const chartMetrics = ["temperature", "humidity", "lux", "rawVal"] as const;
type Metric = (typeof chartMetrics)[number];

export default function Home() {
  const [data, setData] = useState<PiResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [history, setHistory] = useState<Record<string, PiData[]>>({});
  const [selectedMetrics, setSelectedMetrics] = useState<Record<string, Metric>>({});

  useEffect(() => {
    const loadData = async () => {
      try {
        const latest = await getCurrentPiData();
        setData(latest);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching Pi data", err);
      }
    };

    const loadHistory = async () => {
      const ids = ["raspPi1", "raspPi2"];
      const tempHistory: Record<string, PiData[]> = {};

      for (const id of ids) {
        try {
          const readings = await fetchPiHistory(id, "hour");
          tempHistory[id] = readings.slice(-10);
        } catch (err) {
          console.error(`Failed to load history for ${id}`, err);
        }
      }

      setHistory(tempHistory);
    };

    loadData();
    loadHistory();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleMetricChange = (piId: string, newMetric: Metric) => {
    setSelectedMetrics((prev) => ({ ...prev, [piId]: newMetric }));
  };

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-3xl font-bold text-white">Current Sensor Readings</h1>
      {loading ? (
        <p className="text-white">Loading...</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {data.map((pi) =>
            "error" in pi ? (
              <Card key={pi.pieId}>
                <h2 className="text-xl font-bold text-red-500">{pi.pieId} — Offline</h2>
                <p className="text-red-400">Unable to fetch data from this device.</p>
              </Card>
            ) : (
              <Card key={pi.pieId}>
                <h2 className="text-xl font-semibold">{pi.pieId}</h2>
                <p>Temperature: {pi.temperature}°C</p>
                <p>Humidity: {pi.humidity}%</p>
                <p>Pressure: {pi.pressure} hPa</p>
                <p>Gas Resistance: {"gas resistance" in pi ? pi["gas resistance"] : "N/A"} Ω</p>
                <p>Lux: {pi.lux}</p>
                <p>Voltage: {pi.volts} V</p>

                {history[pi.pieId] && (
                  <div className="mt-4 space-y-2">
                    <div className="flex items-center space-x-2">
                      <label htmlFor={`metric-${pi.pieId}`} className="text-sm font-medium">
                        Chart Metric:
                      </label>
                      <select
                        id={`metric-${pi.pieId}`}
                        value={selectedMetrics[pi.pieId] || "temperature"}
                        onChange={(e) =>
                          handleMetricChange(pi.pieId, e.target.value as Metric)
                        }
                        className="bg-gray-800 text-white border border-gray-600 rounded p-1"
                      >
                        {chartMetrics.map((metric) => (
                          <option key={metric} value={metric}>
                            {metric.charAt(0).toUpperCase() + metric.slice(1)}
                          </option>
                        ))}
                      </select>
                    </div>

                    <LineChart
                      title={`${selectedMetrics[pi.pieId] || "temperature"} (last 10)`}
                      data={{
                        labels: history[pi.pieId].map((r) =>
                          new Date(r.timestamp).toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                          })
                        ),
                        datasets: [
                          {
                            label: selectedMetrics[pi.pieId] || "temperature",
                            data: history[pi.pieId].map((r) =>
                              r[selectedMetrics[pi.pieId] || "temperature"]
                            ),
                            borderColor: "rgb(75,192,192)",
                            backgroundColor: "rgba(75,192,192,0.2)",
                            tension: 0.2,
                          },
                        ],
                      }}
                    />
                  </div>
                )}
              </Card>
            )
          )}
        </div>
      )}
    </div>
  );
}
