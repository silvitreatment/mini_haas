from __future__ import annotations


def test_full_api_flow(client):
    dc_resp = client.post("/datacenters", json={"name": "VLADIMIR"})
    assert dc_resp.status_code == 201

    model_resp = client.post(
        "/server-models",
        json={"name": "Dell-R740-64c-512g-4tb", "cpu_cores": 64, "ram_gb": 512, "nvme_tb": 4.0},
    )
    assert model_resp.status_code == 201

    server_resp_1 = client.post(
        "/servers",
        json={"barcode": "SRV-0001", "datacenter": "VLADIMIR", "model_name": "Dell-R740-64c-512g-4tb"},
    )
    assert server_resp_1.status_code == 201

    order_resp = client.post(
        "/orders",
        json={"datacenter": "VLADIMIR", "cpu_cores": 64, "ram_gb": 512, "nvme_tb": 2.0},
    )
    assert order_resp.status_code == 201
    order_id = order_resp.get_json()["id"]

    allocate_resp = client.post(f"/orders/{order_id}/allocate")
    assert allocate_resp.status_code == 200

    provision_resp = client.post(f"/orders/{order_id}/provision")
    assert provision_resp.status_code == 200

    run_resp = client.post("/provision/run-once")
    assert run_resp.status_code == 200

    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 200
