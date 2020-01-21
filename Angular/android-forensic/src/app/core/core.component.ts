import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-core',
  templateUrl: './core.component.html',
  styleUrls: ['./core.component.css']
})
export class CoreComponent implements OnInit {
  headerTitle = "maf tool"
  constructor() { }
  ngOnInit() {
    let list = window.location.href.split("/");
    this.headerTitle = list[list.length -1].replace("-"," ");
    console.log(this.headerTitle);
    
  }
  onButtonGroupClick(event) {
    const clickedElement = event.target || event.srcElement;
    if (clickedElement.nodeName === 'A') {
      const isCertainButtonAlreadyActive = clickedElement.parentElement.parentElement.querySelector('.active');
      if (isCertainButtonAlreadyActive) {
        isCertainButtonAlreadyActive.classList.remove('active');
      }
      clickedElement.parentElement.className += 'active';
      this.headerTitle = clickedElement.parentElement.textContent;
    }
  }

}
