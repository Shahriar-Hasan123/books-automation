.PHONY: test report-html report-allure clean

test:
	pytest -v

report-html:
	xdg-open reports/report.html

report-allure:
	./allure.sh generate allure-results --clean -o allure-report
	./allure.sh open allure-report

clean:
	rm -rf reports/ allure-results/ allure-report/ screenshots/