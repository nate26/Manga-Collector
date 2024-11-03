defmodule MangaServiceWeb.VolumesController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.Volumes

  def index(conn, _params) do
    volumes = Volumes.list_volumes_in_series(conn.params["series_id"], conn.params["limit"], conn.params["offset"])
    render(conn, :index, volumes: volumes)
  end

  def show(conn, %{"isbn" => isbn}) do
    volume = Volumes.get_volume_by_isbn!(isbn)
    render(conn, :show, volume: volume)
  end
end
