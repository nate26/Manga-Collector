defmodule MangaServiceWeb.VolumesJSON do
  alias MangaService.VolumesDB.Volume

  def index(%{volumes: volumes}) do
    %{data: for(volume <- volumes, do: data(volume))}
  end

  def show(%{volume: volume}) do
    case volume do
      nil -> raise "No record found for ISBN"
      _ -> %{data: data(volume)}
    end
  end

  defp data(%Volume{} = datum) do
    %{
      id: datum.id,
      name: datum.name,
      format: datum.format,
      description: datum.description,
      category: datum.category,
      url: datum.url,
      isbn: datum.isbn,
      brand: datum.brand,
      series: datum.series,
      series_id: datum.series_id,
      edition: datum.edition,
      edition_id: datum.edition_id,
      display_name: datum.display_name,
      volume: datum.volume,
      release_date: datum.release_date,
      publisher: datum.publisher,
      pages: datum.pages,
      authors: datum.authors,
      isbn_10: datum.isbn_10,
      primary_cover_image: datum.primary_cover_image,
      cover_images: datum.cover_images,
      inserted_at: datum.inserted_at,
      updated_at: datum.updated_at
    }
  end

end
