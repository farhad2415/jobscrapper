from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from .models import AvilableUrl, Job
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from selenium.common.exceptions import TimeoutException, WebDriverException

def scrape_job_details(url, max_pages):
    base_url = url.strip()
    service = Service('/usr/bin/chromedriver')
    options = Options()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(service=service, options=options)

    data = {
        "is_success": False,
        'url': url,
        'total_jobs': 0,
        'total_skipped_jobs': 0
    }
    total_skipped_jobs = 0
    if base_url == "https://jobsinmalta.com/jobs":
        try:
            for page_number in range(1 , max_pages + 1):
                url = f"{base_url}/page:{page_number}/"
                print(f"Scraping URL: {url}") 

                driver.get(url)
                if "No results found" in driver.page_source:
                    print(f"No more pages found after page {page_number-1}.")
                    break
                job_grid_elements = driver.find_elements(By.CLASS_NAME, 'mobile-job-grid')
                if job_grid_elements:
                    for job_element in job_grid_elements:
                        position = job_element.find_element(By.TAG_NAME, 'h2').text
                        company = job_element.find_element(By.CLASS_NAME, 'job-sub-title').text
                        print(f"Position: {position}")
                        # scraped_data = Job(position=position, company=company)
                        # scraped_data.save()
                        if not Job.objects.filter(position=position, company=company).exists():
                            scraped_data = Job(position=position, company=company)
                            scraped_data.save()
                        else:
                            total_skipped_jobs += 1
                        data = {
                        "is_success": True,
                        'url': url,
                        'total_jobs': len(job_grid_elements),
                        'total_skipped_jobs': total_skipped_jobs
                        }
                else:
                    print(f"No job elements found on page {page_number}.")
            return data
        # if an error occurs while permission denied
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()

    if base_url == "https://www.olx.ro/oferte/q-%C3%AEngrijitor-de-animale/":
        data = {
            "is_success": False,
            'url': url,
            'total_jobs_found': 0,
            'total_skipped_jobs': 0
        }
        try:
            for page_number in range(1, max_pages + 1):
                url = f"{base_url}?page={page_number}"
                print(f"Scraping URL: {url}")

                driver.get(url)
                page_source = driver.page_source
                if "Nu am găsit niciun rezultat" in page_source:
                    print(f"No more pages found after page {page_number-1}.")
                    break
                page_source = BeautifulSoup(page_source, 'html.parser')
                job_grid_elements = page_source.find_all("div", class_='css-j0t2x2')
                
                if not job_grid_elements:
                    print(f"No job elements found on page {page_number}.")
                    continue
                job_element = job_grid_elements[0]
                data_processed = False
                for index, content in enumerate(job_element.contents):
                    if index % 4 == 0:  # Skip index 0, 4, 8, etc.
                        continue
                    
                    job_position = content.find("h6").get_text(strip=True) if content.find("h6") else "Position not found"
                    job_salary = content.find("p").get_text(strip=True) if content.find("p") else "Salary not found"
                    job_location = content.find_all("p")[1].get_text(strip=True) if len(content.find_all("p")) > 1 else "Location not found"
                    job_type = content.find_all("p")[2].get_text(strip=True) if len(content.find_all("p")) > 2 else "Type not found"
                    job_type = content.find_all("p")[2].get_text(strip=True) if len(content.find_all("p")) > 2 else "Type not found"
                        

                    if not Job.objects.filter(position=job_position, salary=job_salary, location=job_location, job_type=job_type).exists():
                        scraped_data = Job(position=job_position, salary=job_salary, location=job_location, job_type=job_type)
                        scraped_data.save()
                        data_processed = True  # Set flag to True if data is processed
                        total_jobs_found += 1
                    # Show a message if any data was processed
                    if data_processed:
                        print("Data has been processed and saved.")
                    else:
                        total_skipped_jobs += 1
            data = {
                "is_success": True,
                'url': url,
                'total_jobs_found': total_jobs_found,
                'total_skipped_jobs': total_skipped_jobs
            }
            return data     
        finally:
            try:
                driver.quit()
            except WebDriverException as e:
                print(f"WebDriverException: {e}")
            except PermissionError as e:
                print(f"PermissionError: {e}. Unable to terminate the WebDriver process.")
            except Exception as e:
                print(f"An unexpected error occurred while quitting the driver: {e}")
       

def scrape_job(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        max_pages = int(request.POST.get('max_pages'))
        if url:
            try:
                scrape_job_details(url, max_pages)  # Assuming this function is defined elsewhere
                data = scrape_job_details(url, max_pages)
                if data['is_success']:
                    messages.success(request, f"Scraping completed successfully! Scraped {data['total_jobs_found']} jobs from {data['url']}. Skipped {data['total_skipped_jobs']} jobs.")
                else:
                    messages.error(request, f"Invalid Url given ::{data['url']}.")
                # messages.success(request, "Scraping completed successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "No URL provided.")
            return JsonResponse({'error': 'No URL provided'}, status=400)

    all_available_urls = AvilableUrl.objects.all()
    return render(request, 'store_job.html', {'all_available_urls': all_available_urls})


# scrape_view make function for view all job data and render to template job_scraper.html
def scrape_view(request):
    jobs = Job.objects.all() 
    paginator = Paginator(jobs, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'job_scraper.html', {'page_obj': page_obj})

def home(request):
    return render(request, 'home.html')