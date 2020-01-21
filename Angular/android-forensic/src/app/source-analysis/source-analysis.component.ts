import { Component, OnInit } from '@angular/core';
import { ForensicReportList, ForensicReport, DetailReport } from '../app.model';
import { AppService } from '../service/app.service';

@Component({
  selector: 'app-source-analysis',
  templateUrl: './source-analysis.component.html',
  styleUrls: ['./source-analysis.component.css']
})
export class SourceAnalysisComponent implements OnInit {

  reportDetail: DetailReport;
  constructor(private appService: AppService) { }

  ngOnInit() {
    this.appService.currentDetailReport.subscribe(data => {
      this.reportDetail = data;
    });
  }
  checkPermission(permissions: string): boolean{
    if(permissions.includes("*")){
      return true;
    }else{
      return false;
    }
  }

}
