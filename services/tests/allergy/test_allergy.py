from services.tests.general import request_base, url_base

url = f"{url_base}/allergy-info/allergy"
data = {"text_allergy": "", "model": "gpt-4o-mini"}


def test_correct_results_pet_fur():
    data["text_allergy"] = "Pelos de gatos e cachorros, ainda mais aqueles com pelos maiores, acabam comigo, sempre espirro muito, sinto os olhos lacrimejando e fico com certa dificuldade de respirar por conta de ficar todo entupido, é terrível."

    response = request_base(url, data)
    return_data = response.json()

    alerts_data = return_data["data"]["allergies"]["alerts"]

    assert response.status_code == 200
    assert "pelos de gatos" in alerts_data["causes"]
    assert "pelos de cachorros" in alerts_data["causes"]
    assert "pelos de animais" in alerts_data["reason_return"]


def test_correct_result_medicine():
    data["text_allergy"] = "Não posso tomar alguns remédios como dipirona e nimesulida por me fazerem mal."

    response = request_base(url, data)
    return_data = response.json()

    medicines_data = return_data["data"]["allergies"]["medicines"]
    alerts_data = return_data["data"]["allergies"]["alerts"]

    assert response.status_code == 200
