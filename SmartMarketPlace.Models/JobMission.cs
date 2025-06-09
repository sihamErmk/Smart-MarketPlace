using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace SmartMarketPlace.Models
{
    public class JobMission
    {
        [JsonPropertyName("title")]
        public string Title { get; set; }
        
        [JsonPropertyName("description")]
        public string Description { get; set; }
        
        [JsonPropertyName("country")]
        public string Country { get; set; }
        
        [JsonPropertyName("city")]
        public string City { get; set; }
        
        [JsonPropertyName("workMode")]
        public string WorkMode { get; set; }
        
        [JsonPropertyName("duration")]
        public int Duration { get; set; }
        
        [JsonPropertyName("durationType")]
        public string DurationType { get; set; }
        
        [JsonPropertyName("startImmediately")]
        public bool StartImmediately { get; set; }
        
        [JsonPropertyName("startDate")]
        public string StartDate { get; set; }
        
        [JsonPropertyName("experienceYear")]
        public string ExperienceYear { get; set; }
        
        [JsonPropertyName("contractType")]
        public string ContractType { get; set; }
        
        [JsonPropertyName("estimatedDailyRate")]
        public int? EstimatedDailyRate { get; set; }
        
        [JsonPropertyName("domain")]
        public string Domain { get; set; }
        
        [JsonPropertyName("position")]
        public string Position { get; set; }
        
        [JsonPropertyName("requiredExpertises")]
        public List<string> RequiredExpertises { get; set; }
    }
    
    public class JobMissionRequest
    {
        public string Prompt { get; set; }
        public string Language { get; set; } = "english";
    }
    
    public class ErrorResponse
    {
        public string Error { get; set; }
        public string RawResponse { get; set; }
    }
}