export class ForensicReportList{
    public data : ForensicReport[];
    constructor(){
        this. data = [];
    }
}
export class DetailReport{
    public obj_id: number;
    public name: string;
    public mtime: string;
    public atime: string;
    public ctime: string;
    public crtime: string;
    public size: string;    
    public appName: string;
    public packageName: string;
    public androidversionCode: string;
    public androidversionName: string;
    public path2Icon: string;
    public cert: string;    
    public MD5: string;
    public SHA1: string;
    public SHA256: string;
    public sendBroadcast: number;
    public onReceive: number;
    public startService: number;
    public onHandleIntent: number;
    public startActivity: number;
    public getIntent: number;  
    public Components: Component[] = []; 
    public Permissions: Permission[] = [];
    public emails: Email[] = [];
    public urls: Url[] = [];
    public ips: Ip[] = [];
    public recovered_file: PathFile[] = [];
}
export class DetailReportList{
    public data : DetailReport[];
    constructor(){
        this. data = [];
    }
}
export class ForensicReport{
    public obj_id: number;
    public current_times: string;
    public total_times: string;
    public type: string;
    public section: string;
    public path_to_source: string;
    public size_in_bytes: string;    
    public AndroidVersion: string;
}
export class WaitingReportList{
    public data : WaitingReport[];
    constructor(){
        this. data = [];
    }
}
export class WaitingReport{
    public id: number;
    public cmd: string;
    public status: any;    
}
export class Component{
    public ComponentName: string;
    public ComponentType: string;
    public ExportStatus: string;
}
export class Permission{
    public PermissionName: string;
}
export class Email{
    public email: string;
}
export class Url{
    public url: string;
}
export class Ip{
    public ip: any;
}
export class PathFile{
    public link_to_file: any;
    public file_name: any;

}
