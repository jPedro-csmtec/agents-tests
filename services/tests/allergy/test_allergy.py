from typing import Any
from services.tests.general import request_base, url_base

url = f"{url_base}/allergy-info/allergy"
data = {"text_allergy": Any, "model": "gpt-4o-mini"}

def test_correct_results_pet_fur():
    data["text_allergy"] = "Pelos de gatos e cachorros, ainda mais aqueles com pelos maiores, acabam comigo, sempre espirro muito, sinto os olhos lacrimejando e fico com certa dificuldade de respirar por conta de ficar todo entupido, é terrível."

    response = request_base(url, data)
    return_data = response.json()

    alerts_data = return_data["data"]["allergies"]["alerts"]

    assert response.status_code == 200
    assert "pelos de gato" in alerts_data["causes"]
    assert "pelos de cachorro" in alerts_data["causes"]
    assert "pelos de animais" in alerts_data["reason_return"]


def test_correct_result_medicine():
    data["text_allergy"] = "Não posso tomar alguns remédios como dipirona e nimesulida por me fazerem mal."

    response = request_base(url, data)
    return_data = response.json()

    medicines_data = return_data["data"]["allergies"]["medicines"]

    assert response.status_code == 200
    assert "nimesulida" in medicines_data["active_ingredients"]
    assert "dipirona" in medicines_data["active_ingredients"]

def test_correct_result_all():
    data["text_allergy"] = "Pelos de gatos e cachorros, ainda mais aqueles com pelos maiores, acabam comigo, sempre espirro muito, sinto os olhos lacrimejando e fico com certa dificuldade de respirar por conta de ficar todo entupido, é terrível. Também não posso tomar alguns remédios como dipirona e nimesulida por me fazerem mal."

    response = request_base(url, data)
    return_data = response.json()

    medicines_data = return_data["data"]["allergies"]["medicines"]
    alerts_data = return_data["data"]["allergies"]["alerts"]

    assert response.status_code == 200
    assert "nimesulida" in medicines_data["active_ingredients"]
    assert "dipirona" in medicines_data["active_ingredients"]
    assert "pelos de gato" in alerts_data["causes"]
    assert "pelos de cachorro" in alerts_data["causes"]
    assert "pelos" in alerts_data["reason_return"]
    assert "espirros" in alerts_data["reason_return"]

def test_error_invalid_input():
    data["text_allergy"] = 500

    response = request_base(url, data)
    result_data = response.json()["detail"][0]

    assert response.status_code == 422
    assert "Input should be a valid string" in result_data["msg"]
