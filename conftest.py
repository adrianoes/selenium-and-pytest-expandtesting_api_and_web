import pytest
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    chromedriver_path = ChromeDriverManager().install()
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")  # Removido para execução visível
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Desabilita o gerenciador de senhas e o prompt de salvar senha
    prefs = {
        "profile.default_content_setting_values.ads": 2,
        "profile.default_content_setting_values.popups": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options)
    try:
        driver.maximize_window()
    except Exception:
        pass
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*ads*", "*doubleclick.net*", "*googlesyndication.com*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.implicitly_wait(5)
    yield driver
    # driver.quit()  # Comentado para manter o navegador aberto para depuração
import pytest

# URL base global para testes web
BASE_URL = "https://practice.expandtesting.com"
import pytest
import os
import json
from datetime import datetime
from pathlib import Path
import base64

# Create directories for test artifacts
ARTIFACTS_DIR = Path("test_artifacts")
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
LOGS_DIR = ARTIFACTS_DIR / "logs"

for directory in [ARTIFACTS_DIR, SCREENSHOTS_DIR, VIDEOS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Store test results for JIRA reporting
test_results = []

def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    config.addinivalue_line(
        "markers", "jira: mark test to create JIRA issue on failure"
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results and create artifacts on failure"""
    outcome = yield
    report = outcome.get_result()
    
    # Only process test call phase (not setup/teardown)
    if report.when == "call":
        test_info = {
            "name": item.nodeid,
            "test_name": item.name,
            "status": report.outcome,
            "duration": report.duration,
            "timestamp": datetime.now().isoformat(),
            "screenshot": None,
            "video": None,
            "log": None,
            "error_message": None,
            "error_traceback": None
        }
        
        if report.failed:
            # Capture error information
            if call.excinfo:
                test_info["error_message"] = str(call.excinfo.value)
                test_info["error_traceback"] = str(call.excinfo.traceback[0].source)  # Convert to string for JSON serialization
            
            # Try to capture screenshot and video from driver
            if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                
                # Capture screenshot
                try:
                    screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    screenshot_path = SCREENSHOTS_DIR / screenshot_name
                    driver.save_screenshot(str(screenshot_path))
                    test_info["screenshot"] = str(screenshot_path)
                    print(f"\n[SCREENSHOT] Saved: {screenshot_path}")
                except Exception as e:
                    print(f"\n[WARNING] Could not capture screenshot: {e}")
        
        # Save detailed log only for failures
        if report.failed:
            log_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_path = LOGS_DIR / log_name
            
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(f"Test: {item.nodeid}\n")
                f.write(f"Status: {report.outcome}\n")
                f.write(f"Duration: {report.duration}s\n")
                f.write(f"Timestamp: {datetime.now()}\n")
                f.write(f"\n{'='*80}\n")
                f.write(f"ERROR MESSAGE:\n")
                f.write(f"{'='*80}\n")
                f.write(f"{test_info['error_message']}\n")
                f.write(f"\n{'='*80}\n")
                f.write(f"TRACEBACK:\n")
                f.write(f"{'='*80}\n")
                if report.longrepr:
                    f.write(str(report.longrepr))
            
            test_info["log"] = str(log_path)
            print(f"[LOG] Saved: {log_path}")
        
        test_results.append(test_info)
        
        # Store in item for access in other hooks
        setattr(item, 'test_result', test_info)

def pytest_sessionfinish(session, exitstatus):
    """Save test results to JSON file at end of session"""
    results_file = ARTIFACTS_DIR / "test_results.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[RESULTS] Test results saved to: {results_file}")
    
    # Print summary
    total = len(test_results)
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    
    print(f"\n{'='*80}")
    print(f"Test Summary: {total} total | [OK] {passed} passed | [ERROR] {failed} failed")
    print(f"{'='*80}\n")
