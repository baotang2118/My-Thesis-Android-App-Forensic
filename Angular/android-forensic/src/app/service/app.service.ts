import { Injectable, Inject } from '@angular/core';
import { API_URL, API_FORENSIC, API_REPORT_DETAIL, API_DOWNLOAD, API_INSPECT_VIA_UI } from '../app.constant';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { ForensicReportList, DetailReportList, DetailReport, WaitingReportList } from '../app.model';
import { from, Observable, throwError, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  private detailReport = new BehaviorSubject(null);
  currentDetailReport = this.detailReport.asObservable();

  constructor(
    @Inject(API_URL) private apiUrl: string, 
    @Inject(API_FORENSIC) private apiForensic: string, 
    @Inject(API_REPORT_DETAIL) private apiReportDetail: string,
    @Inject(API_DOWNLOAD) private apiDownload: string,
    @Inject(API_INSPECT_VIA_UI) private apiInspect: string,
    private http: HttpClient) {       
    }
    getForensicReport(): Observable<ForensicReportList>{
      return this.http.get<ForensicReportList>(this.apiUrl + this.apiForensic);
    }
    getDetailReport(id: number): Observable<DetailReportList>{
      return this.http.get<DetailReportList>(this.apiUrl + this.apiReportDetail + "?report=" + id);
    }
    setDetailReport(detailReport: DetailReport) {
      this.detailReport.next(detailReport)
    }
    postInspectViaUI(link: string): Observable<any>{
      let headers = new HttpHeaders();
      headers= headers.set('content-type', 'application/x-www-form-urlencoded');
      return this.http.post<any>(this.apiUrl + this.apiInspect, "absolute_path="+link, {headers});
    }
    getInspectViaUI(): Observable<WaitingReportList>{
      return this.http.get<WaitingReportList>(this.apiUrl + this.apiInspect + "?view_queue");
    }

}
