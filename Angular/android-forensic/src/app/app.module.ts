import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AngularFontAwesomeModule } from 'angular-font-awesome/dist';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MafComponent } from './maf/maf.component';
import { CoreComponent } from './core/core.component';
import { CodemirrorModule } from '@ctrl/ngx-codemirror';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MatTreeModule } from '@angular/material/tree';
import {
  MatButtonModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatSelectModule,
  MatSidenavModule,
  MatCardModule,
  MatTableModule,
  MatTab,
  MatTabsModule,
  MatIcon,
} from '@angular/material';
import { OverviewComponent } from './overview/overview.component';
import { SourceAnalysisComponent } from './source-analysis/source-analysis.component';
import { API_URL, API_FORENSIC, API_REPORT_DETAIL, API_DOWNLOAD, API_INSPECT_VIA_UI } from './app.constant';
import { HttpClientModule } from '@angular/common/http';
import { MediaComponent } from './media/media.component';

@NgModule({
  declarations: [
    AppComponent,
    MafComponent,
    CoreComponent,
    OverviewComponent,
    SourceAnalysisComponent,
    MediaComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatCardModule,
    AngularFontAwesomeModule,
    CodemirrorModule,
    FormsModule,
    ReactiveFormsModule,
    MatTreeModule,
    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatSelectModule,
    MatSidenavModule,
    MatCardModule,
    MatTableModule,
    MatTabsModule,
    MatIconModule
  ],
  providers: [
    { provide: API_URL, useValue: API_URL },
    { provide: API_FORENSIC, useValue: API_FORENSIC },
    { provide: API_REPORT_DETAIL, useValue: API_REPORT_DETAIL },
    { provide: API_DOWNLOAD, useValue: API_DOWNLOAD },
    { provide: API_INSPECT_VIA_UI, useValue: API_INSPECT_VIA_UI }

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
