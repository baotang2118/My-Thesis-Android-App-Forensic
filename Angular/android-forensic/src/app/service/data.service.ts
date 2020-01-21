
export function isImage(filename: string): boolean {
    let IMAGE_TYPE: string[] = ['apng', 'bmp', 'gif', 'ico', 'cur', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'png', 'svg', 'webp'];
    let type = filename.split('.')[filename.split('.').length - 1];
    if (IMAGE_TYPE.includes(type)) {
        return true;
    }
    else {
        return false;
    }
}
