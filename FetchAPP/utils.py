from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para iterar sobre uma lista de elementos e retornar um array com o texto de cada elemento
def iterate_list(elements):
    # Inicializa uma lista vazia para armazenar os textos dos elementos
    array_iterated = []
    try:
        # Itera sobre cada elemento na lista de elementos
        for element in elements:
            # Adiciona o texto do elemento ao array
            array_iterated.append(element.text)
    except Exception as e:
        # Caso ocorra algum erro, imprime uma mensagem de erro
        print(f"Erro ao iterar elementos da lista: {e}")
    return array_iterated

# Função para transformar uma lista de strings em um único array
def transform_elements(elements):
    # Inicializa uma lista vazia para armazenar os textos transformados
    transformed_list = []
    try:
        # Itera sobre cada item na lista de elementos
        for item in elements:
            # Divide o item em substrings usando '\n' como delimitador e adiciona ao array transformado
            split_items = item.split("\n")
            transformed_list.extend(split_items)
    except Exception as e:
        # Caso ocorra algum erro, imprime uma mensagem de erro
        print(f"Erro ao transformar elementos: {e}")
    return transformed_list

# Função para converter valores de uma enumeração de PT-BR para EN-US
def convert_to_enum(valor):
    try:
        # Dicionário de mapeamento de valores PT-BR para EN-US
        mapeamento = {
            "Alteração no mês passado": "last_month_changes",
            "Total de Visitas": "total_visits",
            "Taxa de Rejeição": "bounce_rate",
            "Páginas por Visita": "pages_per_visit",
            "Duração Média da Visita": "average_visit_duration",
        }
        # Retorna o valor correspondente no dicionário de mapeamento ou o próprio valor se não estiver mapeado
        return mapeamento.get(valor, valor)
    except Exception as e:
        # Caso ocorra algum erro, imprime uma mensagem de erro
        print(f"Erro ao converter valor para enum: {e}")
        return valor

# Função para buscar e retornar o elemento visível no DOM com o XPath fornecido
def fetch_visible_element(url, driver):
    try:
        # Tentativa de localizar e retornar o primeiro elemento visível com o XPath fornecido
        return driver.find_element(By.XPATH, url)
    except Exception as e :
        # Se ocorrer um erro durante a busca do elemento, imprime uma mensagem de erro
        print(f"Erro ao buscar elementos: {e}")
        # Retorna None para indicar que nenhum elemento foi encontrado
        return None
    
# Função para buscar e retornar o elementos visíveis no DOM com o XPath fornecido
def fetch_visible_elements(url, driver):
    try:
        # Tentativa de localizar e retornar os elementos visíveis com o XPath fornecido
        return driver.find_elements(By.XPATH, url)
    except Exception as e :
        # Se ocorrer um erro durante a busca dos elementos, imprime uma mensagem de erro
        print(f"Erro ao buscar elementos: {e}")
        # Retorna None para indicar que nenhum elemento foi encontrado
        return None
    
# Função para obter informações do site
def get_site_info(driver, wait):
    try:
        # Espera até que o elemento do título do site seja visível na página
        site_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[@class='wa-overview__title']")))
        # Retorna um dicionário com o título do site
        return {"site_title": site_element.text}
    except Exception as e:
        # Caso ocorra algum erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações do site: {e}")
        return None

# Função para obter informações de engajamento de tráfego
def get_traffic_engagement_info(driver, wait):
    try:
        # Espera até que todos os elementos de valor de engajamento de tráfego sejam visíveis na página
        traffic_engagement_value = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//p[@class='engagement-list__item-value']")))
        # Espera até que todos os elementos de nome de engajamento de tráfego sejam visíveis na página
        traffic_engagement_key = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//p[@class='engagement-list__item-name']")))
        # Inicializa um dicionário para armazenar as informações de engajamento de tráfego
        traffic_engagement_info = {}
        # Itera sobre as chaves e valores obtidos e adiciona ao dicionário de informações de engajamento de tráfego
        for key, value in zip(traffic_engagement_key, traffic_engagement_value):
            traffic_engagement_info[convert_to_enum(key.text)] = value.text
        return traffic_engagement_info
    except Exception as e:
        print(f"Erro ao obter informações de engajamento de tráfego: {e}")
        return None

def get_classification_info(driver):
    # Função para obter informações de classificação mundial do site

    try:
        # Encontra o elemento de classificação por país
        classification_by_country = fetch_visible_element("//div[@class='wa-rank-list__item wa-rank-list__item--country']//p[@class='wa-rank-list__value']", driver)
        # Encontra o elemento do país
        country_classification = fetch_visible_element("//div[@class='wa-rank-list__item wa-rank-list__item--country']//div[@class='wa-rank-list__info']//a", driver)
        # Encontra o elemento de classificação por categoria
        category_classification = fetch_visible_element("//div[@class='wa-rank-list__item wa-rank-list__item--category']//div[@class='wa-rank-list__value-container']//p[@class='wa-rank-list__value']", driver)
        # Encontra o elemento de teste de classificação por categoria (substitui '\n' por ' ' para formato legível)
        category_classification_teste = fetch_visible_element("//div[@class='wa-rank-list wa-rank-list--md']//div[@class='wa-rank-list__item wa-rank-list__item--category']//div[@class='wa-rank-list__info']//a", driver)

        return {
            "country_classification": {"classification": classification_by_country.text, "country": country_classification.text},
            "category_classification": {"classification": category_classification.text, "category": category_classification_teste.text.replace("\n", " ")}
        }
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de classificação: {e}")
        return None

def get_keywords_info(driver):
    # Função para obter informações de palavras-chave do site
    try:
        # Encontra todos os elementos de palavras-chave
        keywords = fetch_visible_elements('//div[@class="wa-vectors-list__items"]//span[@class="wa-vectors-list__item wa-vectors-list__item--md"]//span[@class="wa-vectors-list__item-row"]', driver)
        keyword_info = []
        keyword_info_data = []
        for keyword_element in keywords:
            # Divide o texto do elemento em duas partes usando '\n' como delimitador
            keyword_info = keyword_element.text.split("\n")
            
            # Se houver duas partes (ou seja, uma palavra-chave e um acesso por palavra-chave), adiciona ao dicionário
            if len(keyword_info) == 2:
                keyword = keyword_info[0]
                access_by_keyword = keyword_info[1]
                keyword_info_data.append({"keyword": keyword, "access_by_keyword": access_by_keyword})
        return keyword_info_data
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de palavras-chave: {e}")
        return None

def get_traffic_by_gender_info(driver):
    # Função para obter informações de acesso por gênero do site
    try:
        # Encontra todos os elementos de informações de tráfego por gênero
        traffic_by_gender = fetch_visible_elements('//div[@class="wa-demographics__gender"]//ul[@class="wa-demographics__gender-legend"]//li[contains(@class, "wa-demographics__gender-legend-item")]', driver)
        gender_info = []
        gender_info_data = []
        for gender_element in traffic_by_gender:
            # Divide o texto do elemento em duas partes usando '\n' como delimitador
            gender_info = gender_element.text.split("\n")
            # Se houver duas partes (ou seja, um gênero e uma porcentagem), adiciona ao dicionário
            if len(gender_info) == 2:
                gender = gender_info[0]
                percentage = gender_info[1]
                gender_info_data.append({"gender": gender, "percentage": percentage})
        return gender_info_data
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de tráfego por gênero: {e}")
        return None

def get_traffic_by_age_info(driver):
    # Função para obter informações de acesso por faixa etária do site
    try:
        # Faixas etárias predefinidas
        age_ranges = ["18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65+"]
        # Encontra todos os elementos de distribuição de idade
        age_distribution = fetch_visible_elements("""
            //*[local-name()='svg' and @class='highcharts-root']
            //*[local-name()='g' and @class='highcharts-data-labels highcharts-series-0 highcharts-column-series highcharts-tracker']
            //*[local-name()='g' and contains(@class, 'highcharts-label highcharts-data-label highcharts-data-label-color-')]
            //*[local-name()='text']
        """, driver)
        traffic_age_info = []
        for index, age_range in enumerate(age_ranges):
            # Obtém a porcentagem para cada faixa etária
            percentage = age_distribution[index].text
            # Adiciona a faixa etária e sua porcentagem ao dicionário
            traffic_age_info.append({"type": age_range, "percentage": percentage})
        return traffic_age_info
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de tráfego por faixa etária: {e}")
        return None

def get_traffic_by_social_media_info(driver):
    # Função para obter informações de acesso por redes sociais do site
    try:
        # Encontra todos os elementos de nomes de redes sociais
        redes = fetch_visible_elements('//span[@class="wa-social-media__chart-label-title"]', driver)
        # Encontra todos os elementos de distribuição de idade por rede social
        age_distribution = fetch_visible_elements("""
            //*[local-name()='svg' and @class='highcharts-root']
            //*[local-name()='g' and @class='highcharts-data-labels highcharts-series-0 highcharts-column-series highcharts-tracker']
            //*[local-name()='g' and contains(@class, 'highcharts-label highcharts-data-label highcharts-data-label-color-')]
            //*[local-name()='text']
        """, driver)
        # Itera sobre as redes sociais e suas distribuições de idade correspondentes
        array_redes = iterate_list(redes)
        array_age_distribution = iterate_list(age_distribution)
        
        social_media_info = []
        for i, rede in enumerate(array_redes):
            # Cria um dicionário para cada rede social com seu tipo e porcentagem correspondente
            rede_dict = {
                "type": rede,
                "percentage": array_age_distribution[i + 6]  # Os dados de porcentagem começam no índice 6
            }
            social_media_info.append(rede_dict)
            
        return social_media_info
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de tráfego por mídia social: {e}")
        return None


def get_origin_traffic_info(driver):
    # Função para obter informações de origem de tráfego do site
    try:
        # Encontra os elementos relacionados a tráfego orgânico vs pago
        org_vs_pg = fetch_visible_elements('//div[@class="wa-keywords__organic-paid-chart-container"]//div[@class="wa-keywords__organic-paid-legend"]', driver)
        # Converte a lista de elementos em uma lista de texto e extrai os dados relevantes
        array_org_vs_pg = transform_elements(iterate_list(org_vs_pg))
        # Organiza as informações de tráfego em uma estrutura de dicionário
        origin_traffic_info = [
            {"type": array_org_vs_pg[0], "percentage": array_org_vs_pg[1]},  # Orgânico
            {"type": array_org_vs_pg[2], "percentage": array_org_vs_pg[3]}   # Pago
        ]
        return origin_traffic_info
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de origem do tráfego: {e}")
        return None

def get_traffic_by_country_info(driver):
    # Função para obter informações dos principais países a acessar o site
    try:
        # Encontra os elementos relacionados ao tráfego por país
        traffic_by_country = fetch_visible_elements("//div[@class='wa-geography__chart']//div//div[@class='wa-legend wa-geography__legend']", driver)
        # Converte a lista de elementos em uma lista de texto e extrai os dados relevantes
        array_country_traffic = transform_elements(iterate_list(traffic_by_country))
        # Organiza as informações de tráfego por país em um dicionário
        traffic_by_country_info = {}
        for i in range(6):
            index = i * 3
            place = i + 1
            traffic_by_country_info[f"country_{place}"] = {
                "country": array_country_traffic[index],
                "percentage": array_country_traffic[index + 1]
            }
        return traffic_by_country_info
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de tráfego por país: {e}")
        return None

def get_traffic_sources_info(driver):
    # Função para obter informações do tipo de acesso ao site
    try:
        # Encontra os elementos relacionados às fontes de tráfego
        fontes = fetch_visible_elements("""
            //*[local-name()='svg' and @class='highcharts-root']
            //*[local-name()='g' and @class='highcharts-data-labels highcharts-series-0 highcharts-column-series highcharts-color-0 highcharts-tracker']
            //*[local-name()='g' and contains(@class, 'highcharts-label highcharts-data-label highcharts-data-label-color-0')]
            //*[local-name()='text']
        """, driver)
        # Converte os elementos em texto e organiza as informações em um dicionário
        array_fontes = [fonte.text for fonte in fontes]
        traffic_sources_info = [
            {"type": "direct", "percentage": array_fontes[0]},
            {"type": "top_referal_traffic", "percentage": array_fontes[1]},
            {"type": "organic_search", "percentage": array_fontes[2]},
            {"type": "paid_search", "percentage": array_fontes[3]},
            {"type": "social", "percentage": array_fontes[4]},
            {"type": "email", "percentage": array_fontes[5]},
            {"type": "display", "percentage": array_fontes[6]}
        ]
        return traffic_sources_info
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações de fontes de tráfego: {e}")
        return None

def get_competitors_info(driver):
    # Função para obter informações dos principais concorrentes do site
    try:
        # Encontra os elementos relacionados aos concorrentes
        competidor_mensal_visits = fetch_visible_elements("//span[@class='wa-competitors__list-column']", driver)
        competidor_ranking = fetch_visible_elements("//span[@class='wa-competitors__list-column wa-competitors__list-column--category-rank']", driver)
        # Organiza as informações dos concorrentes em um dicionário
        competitors_info = {}
        for i in range(10):
            position = i + 1
            index = i * 3
            competitor = {
                "site": competidor_mensal_visits[index].text,
                "monthly_views": competidor_mensal_visits[index + 2].text,
                "ranking": competidor_ranking[i].text
            }
            competitors_info[f"place_{position}"] = competitor
        return competitors_info
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro
        print(f"Erro ao obter informações dos concorrentes: {e}")
        return None

# Definição da função para extrair informações sobre o público-alvo do site
def get_target_audience_info(driver):
    # Tenta buscar as informações sobre o público-alvo do site
    try:
        # Localiza os elementos que contêm as informações sobre o público-alvo usando XPath
        target = fetch_visible_elements("//div[@class='wa-interests__chart-content']", driver)
        # Transforma os elementos em uma lista
        array_target = transform_elements(iterate_list(target))

        # Separa as informações sobre o público-alvo e os tópicos principais
        target_audience = array_target[:5]
        main_topics = array_target[5:]

        # Cria dicionários para armazenar as informações coletadas
        target_audience_data = {f"{i + 1}th_place": value for i, value in enumerate(target_audience)}
        main_topics_data = {f"{i + 1}th_place": value for i, value in enumerate(main_topics)}

        # Retorna um dicionário contendo as informações sobre o público-alvo e os tópicos principais
        return {"target_audience": target_audience_data, "main_topics": main_topics_data}
    
    # Captura exceções que possam ocorrer durante a extração das informações
    except Exception as e:
        # Imprime uma mensagem de erro caso ocorra uma exceção
        print(f"Erro ao obter informações do público-alvo: {e}")
        # Retorna None em caso de erro
        return None


# Definição da função para extrair informações do site
def get_website_info(url):
    # Tenta obter as informações do site
    try:
        # Configurações para o navegador Firefox em modo headless
        options = Options()
        options.headless = True
        # Inicializa o driver do navegador Firefox
        driver = webdriver.Firefox(options=options)
        # Abre a URL especificada
        driver.get(url)

        # Aguarda até que a página seja completamente carregada
        wait = WebDriverWait(driver, 20)

        # Chama várias funções para extrair diferentes tipos de informações do site
        site_info = get_site_info(driver, wait)
        traffic_engagement_info = get_traffic_engagement_info(driver, wait)
        classification_info = get_classification_info(driver)
        keywords_info = get_keywords_info(driver)
        traffic_by_gender_info = get_traffic_by_gender_info(driver)
        traffic_by_age_info = get_traffic_by_age_info(driver)
        traffic_by_social_media_info = get_traffic_by_social_media_info(driver)
        origin_traffic_info = get_origin_traffic_info(driver)
        traffic_by_country_info = get_traffic_by_country_info(driver)
        traffic_sources_info = get_traffic_sources_info(driver)
        competitors_info = get_competitors_info(driver)
        target_audience_info = get_target_audience_info(driver)

        # Encerra a sessão do navegador
        driver.quit()

        # Cria um dicionário contendo todas as informações coletadas do site
        website_info = {
            "site_info": site_info,
            "traffic_engagement_info": traffic_engagement_info,
            "classification_info": classification_info,
            "keywords_info": keywords_info,
            "traffic_by_gender_info": traffic_by_gender_info,
            "traffic_by_age_info": traffic_by_age_info,
            "traffic_by_social_media_info": traffic_by_social_media_info,
            "origin_traffic_info": origin_traffic_info,
            "traffic_by_country_info": traffic_by_country_info,
            "traffic_sources_info": traffic_sources_info,
            "competitors_info": competitors_info,
            "target_audience_info": target_audience_info
        }

        # Retorna o dicionário com as informações do site
        return website_info
    
    # Captura exceções que possam ocorrer durante a extração das informações do site
    except Exception as e:
        # Imprime uma mensagem de erro caso ocorra uma exceção
        print(f"Ocorreu um erro ao obter informações do site: {e}")
        # Retorna None em caso de erro
        return None
