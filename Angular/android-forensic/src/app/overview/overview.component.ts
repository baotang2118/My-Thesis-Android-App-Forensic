import { Component, OnInit } from '@angular/core';
import { ForensicReportList, ForensicReport, DetailReport } from '../app.model';
import { AppService } from '../service/app.service';
import { isImage } from '../service/data.service';
@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent implements OnInit {
  reportDetail: DetailReport;
  cert: string[] = [];
  publicKey: string;
  publicKeyList: string[] = [];
  checkImage = isImage; 
  constructor(private appService: AppService) {}
  ngOnInit() {
    this.appService.currentDetailReport.subscribe(data => {
      this.reportDetail = data;
      if(this.reportDetail){
        this.cert = this.formatCert(this.reportDetail.cert);     
        this.formatCert(this.reportDetail.cert);
        this.publicKeyList = this.publicKey.replace("b'","").replace("'","").split('\\n');               
      }  
    });
  }
  formatCert(cert: string){
    let tempList = cert.split('\n');
    tempList.forEach(async (e, index) =>{
      if(e.includes("Fingerprint")){
        tempList[index] = e.replace("b'","").replace("'","");
      }else if(e.includes('Hash Algorithm')){
        this.publicKey = e;
        tempList.splice(index, 1);   
      }else if(e === ""){
        tempList.splice(index, 1);  
      }
    });
    return tempList;   
  }
}
