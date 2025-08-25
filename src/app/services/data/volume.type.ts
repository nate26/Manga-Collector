export type CoverImage = {
  name: string;
  url: string;
};

export type Volume = {
  id: number;
  isbn: string;
  brand: string;
  display_name: string;
  name: string;
  category: string;
  volume: string;
  url: string;
  release_date: string | null;
  publisher: string | null;
  format: string | null;
  pages: number | null;
  authors: string | null;
  isbn_10: string | null;
  primary_cover_image: string;
  cover_images: CoverImage[];
  description: string;
  edition: string | null;
  edition_id: string | null;
  series: string | null;
  series_id: string;
  inserted_at: string;
  updated_at: string;
};
