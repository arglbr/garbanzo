package garbanzo;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Property implements Serializable
{
	private Integer id;
	private String title;
	private long price;
	private String description;
	private Integer lat;
	
	@JsonProperty("long")
	private Integer _long;

	private Integer beds;
	private Integer baths;
	private Integer squareMeters;

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public long getPrice() {
		return price;
	}

	public void setPrice(long price) {
		this.price = price;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public Integer getLat() {
		return lat;
	}

	public void setLat(Integer lat) {
		this.lat = lat;
	}

	public Integer getLong() {
		return _long;
	}

	public void setLong(Integer _long) {
		this._long = _long;
	}

	public Integer getBeds() {
		return beds;
	}

	public void setBeds(Integer beds) {
		this.beds = beds;
	}

	public Integer getBaths() {
		return baths;
	}

	public void setBaths(Integer baths) {
		this.baths = baths;
	}

	public Integer getSquareMeters() {
		return squareMeters;
	}

	public void setSquareMeters(Integer squareMeters) {
		this.squareMeters = squareMeters;
	}
}

