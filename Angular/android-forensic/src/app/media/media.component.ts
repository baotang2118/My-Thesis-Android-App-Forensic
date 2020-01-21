import { Component, OnInit } from '@angular/core';
import { AppService } from '../service/app.service';
import { PathFile } from '../app.model';
import { DomSanitizer } from '@angular/platform-browser';
import Swal from 'sweetalert2';
import { isImage } from '../service/data.service';

@Component({
  selector: 'app-media',
  templateUrl: './media.component.html',
  styleUrls: ['./media.component.css']
})
export class MediaComponent implements OnInit {
  fileRecover: PathFile[] = [];
  mediaList: PathFile[] = [];
  checkImage = isImage;
  constructor(private appService: AppService, private sanitizer: DomSanitizer) { }
  ngOnInit() {
    this.appService.currentDetailReport.subscribe(data => {
      console.log(data.recovered_file);
      this.mediaList = [];
      this.fileRecover = [];
      data.recovered_file.forEach((e, index) => {
        if (e.file_name.includes('.mp4') ||
          e.file_name.includes('.mp3') || isImage(e.file_name)) {
          this.mediaList.push(e);
        } else {
          this.fileRecover.push(e);
        }
      });
    });
  }
  download(url: string, filename: string) {
    let a = document.createElement("a");
    let nurl = 'http://localhost/api/download.php?file=' + url;
    a.href = nurl;
    a.setAttribute("download", filename);
    a.setAttribute("target", '_blank');
    a.click();
  }
  playAudio(url: string, filename: string) {
    let newHTML = '<h4 style="text-align: center; color: #88d906">'+filename+'</h4><audio style="width:350px; border-radius: 25px" controls><source src="' + url + '">Your browser does not support the audio element.</audio>';
    Swal.fire({
      html: newHTML,
      confirmButtonText: 'Close',
      confirmButtonColor: 'rgb(99, 159, 2)'
    });
  }
}
