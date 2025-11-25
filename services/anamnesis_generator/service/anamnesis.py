import asyncio
from typing import Any, Awaitable, Callable, Literal, Tuple
import uuid

from configurations.config import Config
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from io import StringIO

import xml.etree.ElementTree as ET

from services.agent_allergy.services.allergy import allergy_info
from services.agent_cid_analysis.services.analysis import analysis_info
from services.agent_diagnostic.services.diagnostic import diagnostic_info
from services.agent_extraction.app.schemas.extract_object import ExtractObject, Source
from services.agent_extraction.services.extraction import extract_info
from services.agent_planner.services.intervation_planner import planner_call
from services.agent_resume.services.resume import resume_call
from services.agent_summary.app.schemas.summary_object import RequestSummary
from services.agent_summary.services.summary import summary_call
from services.agent_treatment.services.treatment import treatment_call
from services.anamnesis_generator.app.schemas.file_object import ExtractionFileInfo
from services.anamnesis_generator.app.schemas.summary_input import SummaryInputData

@log_function_call
def build_data(summary_input_data: SummaryInputData) -> dict:
    xml_pacient = ET.Element("PacienteInformacoes")
    raw_result = ""
    files = None
    xml_anamnesis = ET.Element("Anamnesis")
    xml_exames = ET.Element("Exame")
    xml_bio_impendance = ET.Element("BioImpedance")
    xml_result = {}
    
    if (summary_input_data.patient_entity != None):
        ET.SubElement(xml_pacient, "BirthDate").text = str(summary_input_data.patient_entity.birth_date)
        ET.SubElement(xml_pacient, "Genre").text = str(summary_input_data.patient_entity.genre)
        ET.SubElement(xml_pacient, "NameBreedColor").text = str(summary_input_data.patient_entity.name_breed_color)
        ET.SubElement(xml_pacient, "Nationalities").text = str(summary_input_data.patient_entity.nationalities)
        ET.SubElement(xml_pacient, "Address").text = str(summary_input_data.patient_entity.address)
        ET.SubElement(xml_pacient, "Number").text = str(summary_input_data.patient_entity.number)
        ET.SubElement(xml_pacient, "Complement").text = str(summary_input_data.patient_entity.complement)
        ET.SubElement(xml_pacient, "Neighborhood").text = str(summary_input_data.patient_entity.neighborhood)
        ET.SubElement(xml_pacient, "NeighborhoodType").text = str(summary_input_data.patient_entity.neighborhood_type)
        ET.SubElement(xml_pacient, "StateAddress").text = str(summary_input_data.patient_entity.state_address)
        ET.SubElement(xml_pacient, "ZipCode").text = str(summary_input_data.patient_entity.zip_code)
        ET.SubElement(xml_pacient, "City").text = str(summary_input_data.patient_entity.city)
        
        raw_result += f"""
            Paciente Informações:\n
            Cpf: {summary_input_data.patient_entity.cpf}\n
            Nome do Paciente: {summary_input_data.patient_entity.patient_name}\n
            Nome da Mãe: {summary_input_data.patient_entity.mother_name}\n
            Data Nascimento: {summary_input_data.patient_entity.birth_date}\n
            Telefone(Casa): {summary_input_data.patient_entity.home_phone}\n
            DDD: {summary_input_data.patient_entity.ddd_home_phone}\n
            Gênero: {summary_input_data.patient_entity.genre}\n
            Endereço: {summary_input_data.patient_entity.address}\n
            Número: {summary_input_data.patient_entity.number}\n
            Complemento: {summary_input_data.patient_entity.complement}\n
            Vizinhaça: {summary_input_data.patient_entity.neighborhood}\n
            Estado: {summary_input_data.patient_entity.state_address}\n
            Código Postal: {summary_input_data.patient_entity.zip_code}\n
            Cidade: {summary_input_data.patient_entity.city}\n
            Identidade: {summary_input_data.patient_entity.identity}\n
            Empresa Emissora de Identidade: {summary_input_data.patient_entity.identity_issuing_company}\n
            UF da Identidade: {summary_input_data.patient_entity.identity_uf}\n
            Data de Emissão da Identidade: {summary_input_data.patient_entity.identity_issuance_date}\n\n
        """

    if (summary_input_data.anamnesis_entity != None):
        ET.SubElement(xml_anamnesis, "CareUnitDescription").text = str(summary_input_data.anamnesis_entity.care_unit_description)
        ET.SubElement(xml_anamnesis, "ProfessionalName").text = str(summary_input_data.anamnesis_entity.professional_name)
        ET.SubElement(xml_anamnesis, "ModifiedDateTime").text = str(summary_input_data.anamnesis_entity.modified_date_time)
        ET.SubElement(xml_anamnesis, "IaAnamnesisEntity").text = str(summary_input_data.anamnesis_entity.ia_anamnesis_entity)
        
        last_anamnesis = ET.SubElement(xml_anamnesis, "LastAnamnesis")
        ET.SubElement(last_anamnesis, "Saturation").text = str(summary_input_data.anamnesis_entity.last_anamnesis.saturation)
        
        vital_signs = ET.SubElement(last_anamnesis, "VitalSigns")
        ET.SubElement(vital_signs, "Weight").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.weight)
        ET.SubElement(vital_signs, "Height").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.height)
        ET.SubElement(vital_signs, "CardioFrequency").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.cardio_frequency)
        ET.SubElement(vital_signs, "RespiratoryFrequency").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.respiratory_frequency)
        ET.SubElement(vital_signs, "TransesophagealTemp").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.transesophageal_temp)
        ET.SubElement(vital_signs, "BodyTemperature").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.body_temperature)
        ET.SubElement(vital_signs, "Pas").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.pas)
        ET.SubElement(vital_signs, "Pad").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.pad)
        ET.SubElement(vital_signs, "Pam").text = str(summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.pam)
        
        raw_result += f"""
            Anamnesis:\n 
                - Descrição da Unidade de Atendimento: {summary_input_data.anamnesis_entity.care_unit_description}\n
                - Professional Name: {summary_input_data.anamnesis_entity.professional_name}\n
                - Data/Hora de Modificação: {summary_input_data.anamnesis_entity.modified_date_time}\n
            Última Anamnese:
                - Sinais Vitais:
                    Peso: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.weight}\n
                    Altura: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.height}\n
                    Frequência Cardíaca {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.cardio_frequency}\n
                    Frequência Respiratória: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.respiratory_frequency}\n
                    Temperatura Transesofágica: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.transesophageal_temp}\n
                    Temperatura Corporal: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.body_temperature}\n
                    Pas: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.pas}\n
                    Pad: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.pad}\n
                    Pam: {summary_input_data.anamnesis_entity.last_anamnesis.vital_signs.pam}\n
                - Saturação: {summary_input_data.anamnesis_entity.last_anamnesis.saturation}\n
                - Entrevista: {summary_input_data.anamnesis_entity.ia_anamnesis_entity}\n
        """
           
    if (summary_input_data.bioimpedance_entity != None):
        ET.SubElement(xml_bio_impendance, "PercentBodyFat").text = str(summary_input_data.bioimpedance_entity.percent_body_fat)
        ET.SubElement(xml_bio_impendance, "FatMassKg").text = str(summary_input_data.bioimpedance_entity.fat_mass_kg)
        ET.SubElement(xml_bio_impendance, "RestingEnergyExpenditureKcal").text = str(summary_input_data.bioimpedance_entity.resting_energy_expenditure_kcal)
        ET.SubElement(xml_bio_impendance, "BodyWaterPercent").text = str(summary_input_data.bioimpedance_entity.body_water_percent)
        ET.SubElement(xml_bio_impendance, "EvalBodyWaterRate").text = str(summary_input_data.bioimpedance_entity.eval_body_water_rate)
        ET.SubElement(xml_bio_impendance, "SkeletalMusclePercent").text = str(summary_input_data.bioimpedance_entity.skeletal_muscle_percent)
        ET.SubElement(xml_bio_impendance, "EvalSkeletalMuscle").text = str(summary_input_data.bioimpedance_entity.eval_skeletal_muscle)
        ET.SubElement(xml_bio_impendance, "VisceralFatIndex").text = str(summary_input_data.bioimpedance_entity.visceral_fat_index)
        ET.SubElement(xml_bio_impendance, "EvalVisceralFat").text = str(summary_input_data.bioimpedance_entity.eval_visceral_fat)
        ET.SubElement(xml_bio_impendance, "BoneMineralContentKg").text = str(summary_input_data.bioimpedance_entity.bone_mineral_content_kg)
        ET.SubElement(xml_bio_impendance, "EvalBoneMineral").text = str(summary_input_data.bioimpedance_entity.eval_bone_mineral)
        ET.SubElement(xml_bio_impendance, "ExtracellularFluidKg").text = str(summary_input_data.bioimpedance_entity.extracellular_fluid_kg)
        ET.SubElement(xml_bio_impendance, "IntracellularFluidKg").text = str(summary_input_data.bioimpedance_entity.intracellular_fluid_kg)
        ET.SubElement(xml_bio_impendance, "TotalBodyWaterKg").text = str(summary_input_data.bioimpedance_entity.total_body_water_kg)
        ET.SubElement(xml_bio_impendance, "ProteinMassKg").text = str(summary_input_data.bioimpedance_entity.protein_mass_kg)
        ET.SubElement(xml_bio_impendance, "InorganicSaltKg").text = str(summary_input_data.bioimpedance_entity.inorganic_salt_kg)
        ET.SubElement(xml_bio_impendance, "BodyAgeYears").text = str(summary_input_data.bioimpedance_entity.body_age_years)
        ET.SubElement(xml_bio_impendance, "OverallRating").text = str(summary_input_data.bioimpedance_entity.overall_rating)
        
        raw_result += f"""
                Bioimpedância:
                    Percentual de Gordura Corporal: {summary_input_data.bioimpedance_entity.percent_body_fat}\n
                    Massa Gorda Kg: {summary_input_data.bioimpedance_entity.fat_mass_kg}\n
                    Gasto Energético de Repouso Kcal: {summary_input_data.bioimpedance_entity.resting_energy_expenditure_kcal}\n
                    Percentual de Água Corporal: {summary_input_data.bioimpedance_entity.body_water_percent}\n
                    Avaliação da Taxa de Água Corporal: {summary_input_data.bioimpedance_entity.eval_body_water_rate}\n
                    Percentual de Músculo Esquelético: {summary_input_data.bioimpedance_entity.skeletal_muscle_percent}\n
                    Avaliação do Músculo Esquelético: {summary_input_data.bioimpedance_entity.eval_skeletal_muscle}\n
                    Índice de Gordura Visceral: {summary_input_data.bioimpedance_entity.visceral_fat_index}\n
                    Avaliação da Gordura Visceral: {summary_input_data.bioimpedance_entity.eval_visceral_fat}\n
                    Conteúdo Mineral Ósseo Kg: {summary_input_data.bioimpedance_entity.bone_mineral_content_kg}\n
                    Avaliação Mineral Óssea: {summary_input_data.bioimpedance_entity.eval_bone_mineral}\n
                    Fluido Extracelular Kg: {summary_input_data.bioimpedance_entity.extracellular_fluid_kg}\n
                    Fluido Intracelular Kg: {summary_input_data.bioimpedance_entity.intracellular_fluid_kg}\n
                    Água Corporal Total Kg: {summary_input_data.bioimpedance_entity.total_body_water_kg}\n
                    Massa Proteica Kg: {summary_input_data.bioimpedance_entity.protein_mass_kg}\n
                    Sais Inorgânicos Kg: {summary_input_data.bioimpedance_entity.inorganic_salt_kg}\n
                    Idade Corporal Anos: {summary_input_data.bioimpedance_entity.body_age_years}\n
                    Classificação Geral: {summary_input_data.bioimpedance_entity.overall_rating}\n
                """
                
    if (len(summary_input_data.files) > 0):
        files = ET.SubElement(xml_exames, "Files")
        raw_result += "Arquivos:\n"
        for i in summary_input_data.files:
            raw_result += f"Nome:{i.name}\nDescrição:{i.description}"
            
    xml_result['info'] = "\n".join([
        ET.tostring(xml_pacient, encoding="utf-8").decode("utf-8"),
        ET.tostring(xml_anamnesis, encoding="utf-8").decode("utf-8"), 
        ET.tostring(xml_bio_impendance, encoding="utf-8").decode("utf-8"),
        summary_input_data.interview, 
        ET.tostring(xml_exames, encoding="utf-8").decode("utf-8")]
    )
    xml_result['raw_data'] = raw_result
    xml_result['files'] = files
    
    return xml_result

@log_function_call
async def try_sub_stage_calls(function_call: Callable[..., Awaitable[None]]):
    tries = 0
    call = None
    while(tries < int(Config.TRY_CALL_AGENTS)):
        call, status = await function_call
        
        if(status):
            return call, True
        
        tries+=1
        await asyncio.sleep(int(Config.TIME_TO_WAIT))
    return None, False

@log_function_call
async def last_diagnostic(sb:StringIO) -> tuple[Any | None, bool]:
    
    try:
        task=[]
        planner_task = asyncio.create_task(planner_call(sb.getvalue()))
        task.append(planner_task)
        treatment_task = asyncio.create_task(treatment_call(sb.getvalue()))
        task.append(treatment_task)
        (result_planner, _), (result_treatment, _) = await asyncio.gather(*task)
        sb.write("\n".join([result_planner, result_treatment]))
        
        last_diagnostic, status = await try_sub_stage_calls(diagnostic_info({"text_diagnostic":sb.getvalue(), "model":"gpt-4o-2024-08-06"}))
        
    except Exception as e:
        error_message = f"ERRO: {e}"
        return error_message, False
    
    return last_diagnostic, status
    

@log_function_call
async def orchestration_call_agents(payload: dict) -> tuple[str, Literal[False]] | tuple[dict, Literal[True]]:
    
    orchestration_data = {
        'cid':'',
        'cidDescription':'',
        'activeIngredients':'',
        'causes':'',
        'xmlResponse':'',
        'dataRawResponse':'',
        'resultSummary':''
    }
    sb = StringIO()
    try:
        orchestration_data['xmlResponse'] = payload.get('info')
        orchestration_data['dataRawResponse'] = payload.get('raw_data').replace("\n", "<br/>")
        sb.write(payload.get('info'))
        
        result_cid, status = await try_sub_stage_calls(analysis_info(sb.getvalue()))
        if(not status):
            orchestration_data['resultSummary']=payload.get('raw_data')
            return orchestration_data, True
        
        orchestration_data['cid'] = result_cid.cid
        orchestration_data['cidDescription'] = result_cid.result.replace("\n", "<br/>")
        sb.write(result_cid.result)
        
        result_diagnostic, status = await try_sub_stage_calls(diagnostic_info({"text_diagnostic":sb.getvalue(), "model":"gpt-4o-2024-08-06"}))
        if(not status):
            orchestration_data['resultSummary']=payload.get('raw_data').replace("\n", "<br/>")
            return orchestration_data, True
        
        sb.write(result_diagnostic)
         
        result_resumo, status = await try_sub_stage_calls(resume_call(sb.getvalue()))
        if(not status):
            orchestration_data['resultSummary']=result_diagnostic.result.replace("\n", "<br/>")
            return orchestration_data, True
        
        sb.write(result_resumo)
        
        last_diag_result, status = await last_diagnostic(sb)
        if(status):
           sb.write(last_diag_result)
        
        result_allergy, _ = await allergy_info({"text_allergy":payload.get('info')})
        orchestration_data['activeIngredients'] = result_allergy.allergies.medicines.active_ingredients
        orchestration_data['causes'] = result_allergy.allergies.alerts.causes
        
        request_summary = RequestSummary(text_summary=sb.getvalue(), agent_resume=True)
        result_summary_resumo, status = await try_sub_stage_calls(summary_call(request_summary))
        if(not status):
            return orchestration_data, True
        
        orchestration_data['resultSummary'] = result_summary_resumo.replace("\n", "<br/>")
        
    except Exception as e:
        error_message = f"ERRO: {e}"
        send_message_telegram(error_message, "ORCHESTRATION_CALL")
        return error_message, False
    
    return orchestration_data, True

@log_function_call
async def anamnesis_data(payload:SummaryInputData) -> Tuple[str, bool]:
    """
    Função responsavel pela formatação dos dados para processamento da IA.
    Args:
        patient_entity (Patient): Informações do paciente
        historico_atendimento_entity (List[AttendanceHistory]): Lista com historico de atendimento
        anamnesis_entity (Anamnesis): Estrutura de dados da anamnese.
        bioimpedance_entity (AtdSessionBioimpedance): Estrutura de dados da bioimpedancia
        interview (str): Informação da entrevista
    """
    
    try:
        data = build_data(payload)
        result = await orchestration_call_agents(data)
                
    except Exception as e:
        error_message=f"Erro: {e}"
        send_message_telegram(error_message, "ANANMESIS_DATA")
        return error_message, False
    
    return result

@log_function_call
async def anamnesis_extraction(payload:ExtractionFileInfo) -> Tuple[str, bool]:
    """
    Função responsavel por extrair informação de arquivo, em formato de texto.
    Args:
        extract_object (ExtractObject): Informações do paciente
    """
    
    try:
        
        new_payload = {
                        "id": payload.id,
                        "source": {
                            "type": "s3",
                            "url": payload.url,
                            "data": "",
                            "name": payload.name,
                            "extension": payload.extension
                        },
                        "options": {
                            "model": "awsDocumentExtractOcr",
                            "modelOptions": {
                                "type_model": "OCR",
                                "prompt": "",
                                "model_name": "mistral-ocr-2505"
                            }
                        }
                      } 

        anamnesis_file, status = await extract_info(new_payload)
                
    except Exception as e:
        error_message=f"Erro: {e}"
        send_message_telegram(error_message, "ANANMESIS_EXTRACTION")
        return error_message, False
    
    return anamnesis_file, status