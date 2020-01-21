import { Component, OnInit } from '@angular/core';
import 'codemirror/mode/sql/sql';
import { ForensicReport, DetailReport, WaitingReport } from '../app.model';
import { AppService } from '../service/app.service';
import Swal from 'sweetalert2';
import { interval } from 'rxjs';
@Component({
  selector: 'app-maf',
  templateUrl: './maf.component.html',
  styleUrls: ['./maf.component.css']
})
export class MafComponent implements OnInit {
  reportList: ForensicReport[] = [];
  waitingReportList: WaitingReport[] = [];
  reportDetailList: DetailReport[] = [];
  chooseFileIndex: number = 0;
  loadInfoAPK = false;
  reportName: string = '';
  link: string = "";
  lenghtWaitListTemp: number = 0;
  openReport(id: number, reportName) {
    this.appService.getDetailReport(id).subscribe(data => {
      this.reportDetailList = data.data;
      this.appService.setDetailReport(this.reportDetailList[0]);
      this.loadInfoAPK = true;
      this.reportName = 'Report_' + reportName;
    });
  }
  backToReport() {
    this.loadInfoAPK = false;
  }
  byteToGiga(byte: number) {
    let n = byte / 1073741824;
    return Math.round(n * 100) / 100;
  }
  constructor(private appService: AppService) { }
  ngOnInit() {
    this.appService.getForensicReport().subscribe(data => {
      this.reportList = data.data;
    });
    this.appService.getInspectViaUI().subscribe(data => {
      this.lenghtWaitListTemp = data.data.length;
      this.waitingReportList = data.data;
      if (this.waitingReportList.length > 0) {
        interval(10000).subscribe(n => {
          if(this.loadInfoAPK !== true){
            this.appService.getInspectViaUI().subscribe(data => {
              this.waitingReportList = data.data;
              this.waitingReportList.forEach(e => {             
                if (this.lenghtWaitListTemp > data.data.length) {               
                  this.appService.getForensicReport().subscribe(data => {
                    this.reportList = data.data;
                  });
                }
                this.lenghtWaitListTemp = data.data.length;
              })
            });
          }
        });
      }
    });

  }
  onButtonGroupClick(event) {
    const clickedElement = event.target || event.srcElement;
    if (clickedElement.nodeName === 'LI') {
      const isCertainButtonAlreadyActive = clickedElement.parentElement.querySelector('.active');
      if (isCertainButtonAlreadyActive) {
        isCertainButtonAlreadyActive.classList.remove('active');
      }
      clickedElement.className += ' active';
    }
  }
  viewReport(report: DetailReport, index: number) {
    this.appService.setDetailReport(report);
    this.chooseFileIndex = index;
  }
  AnalysisIMGFile(link: string) {
    link = link.replace(/ /g, "_").toLowerCase();
    let name = link.split('.')[link.split('.').length - 1];
    if (name === 'img' || name === 'raw' || name === 'iso' || name === 'dd') {
      this.appService.postInspectViaUI(link).subscribe(data => {
        this.appService.getInspectViaUI().subscribe(data => {
          this.waitingReportList = data.data;
        });
        Swal.fire('Warning!', 'Your new file have been put into the queue to analysis!', 'warning');
      });
    } else {
      Swal.fire('Error!', 'Your file is wrong format!', 'error');
    }
  }
  getWaitingReportName(name: string) {
    return name = name.split('\\')[name.split('\\').length - 1];
  }
  isExistFile(url) {
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status != 404;
  }
}
