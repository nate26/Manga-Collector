import { IManga } from './iManga.interface';

export interface IGQLListMangaRecords {
    list_manga_records: {
        manga_records: IManga[];
    };
}