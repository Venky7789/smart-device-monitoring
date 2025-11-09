const API_BASE = "http://127.0.0.1:5000"; // ✅ Backend endpoint base path

let lastOnlineSet = new Set(); // Track online devices for notifications

// TEMPORARY TEST DATA
async function fetchCompanies() {
  return { companies: [{ id: 1, name: "Company A" }, { id: 2, name: "Company B" }] };
}
async function fetchDevices(companyId) {
  return {
    devices: [
      { id: 1, name: "Sensor 1", status: "online", last_reading: Date.now() },
      { id: 2, name: "Sensor 2", status: "offline", last_reading: null },
      { id: 3, name: "Sensor 3", status: "online", last_reading: Date.now() - 30000 }
    ]
  };
}


function renderDeviceTile(device) {
  const card = document.createElement("div");
  card.className = "device-card";
  const title = document.createElement("div");
  title.className = "device-title";
  title.textContent = device.name;

  const statusRow = document.createElement("div");
  statusRow.className = "status-row";

  const status = document.createElement("div");
  status.className = "status-pill " + (device.status === "online" ? "status-online" : "status-offline");
  status.textContent = device.status.toUpperCase();

  const last = document.createElement("div");
  last.className = "last-time";
  last.textContent = device.last_reading ? new Date(device.last_reading).toLocaleString() : "No readings";

  statusRow.appendChild(status);
  statusRow.appendChild(last);
  card.appendChild(title);
  card.appendChild(statusRow);
  return card;
}

function showNotification(message) {
  const n = document.getElementById("notification");
  n.textContent = message;
  n.classList.remove("hidden");
  setTimeout(() => n.classList.add("hidden"), 5000);
}

async function loadDevicesForCompany(companyId) {
  try {
    const data = await fetchDevices(companyId);
    const devices = data.devices || [];
    const container = document.getElementById("devicesContainer");
    container.innerHTML = "";

    const filter = document.getElementById("filterSelect").value;

    const currentOnlineSet = new Set();
    devices.forEach(d => { if (d.status === "online") currentOnlineSet.add(d.id) });

    for (const id of currentOnlineSet) {
      if (!lastOnlineSet.has(id)) {
        const dev = devices.find(x => x.id === id);
        showNotification(`Device "${dev.name}" is now ONLINE`);
      }
    }
    lastOnlineSet = currentOnlineSet;

    const filtered = devices.filter(d => filter === "all" ? true : d.status === filter);
    if (filtered.length === 0) {
      container.innerHTML = "<p style='grid-column:1/-1;color:#666'>No devices found</p>";
      return;
    }

    filtered.forEach(dev => {
      const node = renderDeviceTile(dev);
      container.appendChild(node);
    });

  } catch (err) {
    console.error(err);
    document.getElementById("devicesContainer").innerHTML = "<p style='color:red'>Failed to load devices</p>";
  }
}

async function init() {
  const cs = document.getElementById("companySelect");
  const filter = document.getElementById("filterSelect");

  try {
    const companiesRes = await fetchCompanies();
    const companies = companiesRes.companies || [];
    cs.innerHTML = "";
    companies.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.name;
      cs.appendChild(opt);
    });

    if (companies.length > 0) {
      cs.value = companies[0].id;
      await loadDevicesForCompany(cs.value);
    } else {
      document.getElementById("devicesContainer").innerHTML = "<p>No companies found</p>";
    }

    cs.addEventListener("change", async (e) => {
      await loadDevicesForCompany(e.target.value);
    });

    filter.addEventListener("change", async () => {
      await loadDevicesForCompany(cs.value);
    });

    setInterval(async () => {
      if (cs.value) await loadDevicesForCompany(cs.value);
    }, 10000);

  } catch (err) {
    console.error(err);
    cs.innerHTML = "<option>Error loading companies</option>";
    document.getElementById("devicesContainer").innerHTML = "<p style='color:red'>Failed to load companies</p>";
  }
}

window.addEventListener("DOMContentLoaded", init);
