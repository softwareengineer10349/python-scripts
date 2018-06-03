import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {GoogleChartComponent} from 'ng2-google-charts';
import {HostListener} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'app';

  constructor(private http: HttpClient){
 }


 drawAllJobGraph(city_name, num_results, skill_type): void {

 this.http.get("http://localhost/job_skills_web_pages/get_all_jobs.php?number_of_results="+num_results+"&city_name="+city_name+"&skill_type="+skill_type).subscribe(data => {

   var arrayOfAllJobs = [
   [data.cols[0].label, data.cols[1].label]
   ];

   for(var i=0; i<data.rows.length; ++i){
   arrayOfAllJobs.push([data.rows[i].c[0].v, data.rows[i].c[1].v]);
   }

   this.dataAllJobs =  {
   chartType: 'BarChart',
   dataTable: arrayOfAllJobs,
   options: {
   width: 1000,
   height: 1000,
   legend :'none',
   'title': 'Most popular skills commercially'
 }
   };
 });

 }


 drawJobSpecificGraph(skill_selected, city_name, num_results, skill_type): void {

 this.http.get('http://localhost/job_skills_web_pages/get_job_numbers.php?table_name=' + skill_selected + '&number_of_results=' + num_results + '&city_name=' + city_name + '&skill_type=' + skill_type).subscribe(data => {
   this.job_numbers = data;

   var arrayOfJobs = [
   [data.cols[0].label, data.cols[1].label]
   ];

   for(var i=0; i<this.job_numbers.rows.length; ++i){
   arrayOfJobs.push([this.job_numbers.rows[i].c[0].v, this.job_numbers.rows[i].c[1].v]);
   }

   this.jobData =  {
   chartType: 'BarChart',
   dataTable: arrayOfJobs,
   options: {
   width: 1000,
   height: 1000,
   legend :'none',
   'title': 'Most popular skills for jobs relating to ' + skill_selected
 }
   };
 });

 }

 setValueIfUndefined(initialValue, toSet): string{
 if(initialValue == undefined){
 return toSet;
 }
 return initialValue;
 }

 recalculateCountSpecificJob(skill, city): void {
 this.http.get('http://localhost/job_skills_web_pages/get_count_total.php?table_name='+ skill +'&city_name=' + city).subscribe(data => {
   this.total_data_count = data.count;
 });
 }

 changeAllJobsGraph(): void{
 this.selectedLocation = this.setValueIfUndefined(this.selectedLocation, this.all_locations[0]);
 this.selectedSkillType = this.setValueIfUndefined(this.selectedSkillType, this.all_skill_types[0]);
 this.selectedAmount = this.setValueIfUndefined(this.selectedAmount, 10);

 this.drawAllJobGraph(this.selectedLocation, this.selectedAmount, this.selectedSkillType);

 }

changeJobSpecificGraph(): void {

this.selectedSkill = this.setValueIfUndefined(this.selectedSkill, this.all_skills[0]);
this.selectedLocation = this.setValueIfUndefined(this.selectedLocation, this.all_locations[0]);
this.selectedSkillType = this.setValueIfUndefined(this.selectedSkillType, this.all_skill_types[0]);
this.selectedAmount = this.setValueIfUndefined(this.selectedAmount, 10);

this.recalculateCountSpecificJob(this.selectedSkill, this.selectedLocation);
this.drawJobSpecificGraph(this.selectedSkill, this.selectedLocation, this.selectedAmount, this.selectedSkillType);

 }


 ngOnInit(): void {

 //console.log("type of data: "+typeof(data));
 //console.log("data: "+JSON.stringify(data));
 //console.log("jsonified 0 = "+data.cols[0].label);
 //console.log("jsonified 0 = "+data.rows[0].c[0].v);
 //console.log("names = "+this.all_skills[0]);

    this.http.get('http://localhost/job_skills_web_pages/get_all_locations.php').subscribe(data => {
      this.all_locations = data.names;
      this.http.get('http://localhost/job_skills_web_pages/get_all_types_skills.php?table_name=Language').subscribe(data => {
        this.all_skill_types = data.names;
        this.http.get('http://localhost/job_skills_web_pages/get_all_skills.php').subscribe(data => {
          this.all_skills = data.names;

          this.recalculateCountSpecificJob(this.all_skills[0], this.all_locations[0]);
          this.drawJobSpecificGraph(this.all_skills[0], this.all_locations[0], 10, this.all_skill_types[0]);
          this.drawAllJobGraph(this.all_locations[0], 10, this.all_skill_types[0]);

        });
      });
    });

}
}
