--ATTACH 'C:\\Users\\si929x\\Desktop\\projects\\multi_agent_demo\\nl2sql-service\\tests\\Chinook.db' AS chinook (TYPE sqlite, READ_ONLY);
ATTACH ':memory:' AS vitas;
USE vitas;
CREATE OR REPLACE SCHEMA sales;
USE vitas.sales;
CREATE OR REPLACE TABLE "tt_balance_order" (
	"id" decimal(10,0),
	"asc_code" varchar,
	"balance_no" varchar,
	"last_balance_no" varchar,
	"ro_no" varchar,
	"ro_type" decimal(1, 0),
	"repair_type" varchar,
	"service_advisor" varchar,
	"start_time" timestamp,
	"chief_technician" varchar,
	"owner_name" varchar,
	"owner_property" decimal(4, 0),
	"license" varchar,
	"vin" varchar,
	"engine_no" varchar,
	"brand" varchar,
	"series" varchar,
	"model" varchar,
	"start_mileage" decimal(8,2),
	"end_mileage" decimal(8,2),
	"deliverer" varchar,
	"deliverer_gender" varchar,
	"deliverer_ddd_code" varchar,
	"deliverer_phone" varchar,
	"deliverer_mobile" varchar,
	"balance_time" timestamp,
	"total_amount" decimal(12,2),
	"is_change_mileage" decimal(1,0),
	"remark" varchar,
	"end_time_supposed" timestamp,
	"claim_no" varchar,
	"complete_time" timestamp,
	"is_valid" decimal(1,0),
	"first_load_date" timestamp,
	"last_load_date" timestamp,
	"load_from" varchar(30)
);
comment on TABLE "tt_balance_order" is '售后工单信息表';
comment on COLUMN "tt_balance_order"."id" is '工单序列号';
comment on COLUMN "tt_balance_order"."asc_code" is '经销商代码';
comment on COLUMN "tt_balance_order"."balance_no" is '结算单号';
comment on COLUMN "tt_balance_order"."last_balance_no" is '原结算单号';
comment on COLUMN "tt_balance_order"."ro_no" is '工单号';
comment on COLUMN "tt_balance_order"."ro_type" is '工单类型:1维修、2销售、3返工、4索赔';
comment on COLUMN "tt_balance_order"."repair_type" is '维修类型';
comment on COLUMN "tt_balance_order"."service_advisor" is '服务顾问';
comment on COLUMN "tt_balance_order"."start_time" is '开单时间';
comment on COLUMN "tt_balance_order"."chief_technician" is '责任技师';
comment on COLUMN "tt_balance_order"."owner_name" is '车主姓名';
comment on COLUMN "tt_balance_order"."owner_property" is '车主性质';
comment on COLUMN "tt_balance_order"."license" is '车牌号';
comment on COLUMN "tt_balance_order"."vin" is 'VIN号';
comment on COLUMN "tt_balance_order"."engine_no" is '发动机号';
comment on COLUMN "tt_balance_order"."brand" is '品牌';
comment on COLUMN "tt_balance_order"."series" is '车系';
comment on COLUMN "tt_balance_order"."model" is '车型';
comment on COLUMN "tt_balance_order"."start_mileage" is '进厂里程';
comment on COLUMN "tt_balance_order"."end_mileage" is '出厂里程';
comment on COLUMN "tt_balance_order"."deliverer" is '送修人姓名';
comment on COLUMN "tt_balance_order"."deliverer_gender" is '送修人性别';
comment on COLUMN "tt_balance_order"."deliverer_ddd_code" is '送修人区号';
comment on COLUMN "tt_balance_order"."deliverer_phone" is '送修人电话';
comment on COLUMN "tt_balance_order"."deliverer_mobile" is '送修人手机号';
comment on COLUMN "tt_balance_order"."balance_time" is '结算时间';
comment on COLUMN "tt_balance_order"."total_amount" is '结算金额';
comment on COLUMN "tt_balance_order"."is_change_mileage" is '换表标识';
comment on COLUMN "tt_balance_order"."remark" is '备注';
comment on COLUMN "tt_balance_order"."end_time_supposed" is '预交车时间';
comment on COLUMN "tt_balance_order"."claim_no" is '索赔单号';
comment on COLUMN "tt_balance_order"."complete_time" is '竣工时间';
comment on COLUMN "tt_balance_order"."is_valid" is '是否有效:1无效、0有效';
comment on COLUMN "tt_balance_order"."first_load_date" is '初次加载时间';
comment on COLUMN "tt_balance_order"."last_load_date" is '末次加载时间';
comment on COLUMN "tt_balance_order"."load_from" is '数据来源';

CREATE OR REPLACE TABLE "tt_balance_item" (
	"id" decimal(11,0),
	"trouble_desc" varchar,
	"trouble_reason" varchar,
	"sgm_labour_code" varchar,
	"labour_name" varchar,
	"std_labour_hour" decimal(10,2),
	"add_labour_hour" decimal(10,2),
	"assign_labour_hour" decimal(10,2),
	"labour_amount" decimal(12,2),
	"labour_price" decimal(6,2),
	"worker_type" varchar,
	"bo_id" decimal(11,0),
	"asc_code" varchar,
	"balance_no" varchar,
	"worker_type_name" varchar,
	"is_valid" decimal(1,0),
	"first_load_date" timestamp,
	"last_load_date" timestamp,
	"load_from" varchar(30)
);
comment on TABLE "tt_balance_item" is '售后项目信息表';
comment on COLUMN "tt_balance_item"."id" is '项目ID';
comment on COLUMN "tt_balance_item"."trouble_desc" is '故障描述';
comment on COLUMN "tt_balance_item"."trouble_reason" is '故障原因';
comment on COLUMN "tt_balance_item"."sgm_labour_code" is 'SGM项目代码';
comment on COLUMN "tt_balance_item"."labour_name" is '项目名称';
comment on COLUMN "tt_balance_item"."std_labour_hour" is '标准工时';
comment on COLUMN "tt_balance_item"."add_labour_hour" is '附加工时';
comment on COLUMN "tt_balance_item"."assign_labour_hour" is '派工工时';
comment on COLUMN "tt_balance_item"."labour_amount" is '工时金额';
comment on COLUMN "tt_balance_item"."labour_price" is '工时单价';
comment on COLUMN "tt_balance_item"."worker_type" is '工种代码';
comment on COLUMN "tt_balance_item"."bo_id" is '工单ID';
comment on COLUMN "tt_balance_item"."asc_code" is 'ASC代码';
comment on COLUMN "tt_balance_item"."balance_no" is '结算单号';
comment on COLUMN "tt_balance_item"."worker_type_name" is '工种代码描述';
comment on COLUMN "tt_balance_item"."is_valid" is '是否有效(1:有效，0:无效，值同源表）代表结算单的有效性，而非项目的有效性';
comment on COLUMN "tt_balance_item"."first_load_date" is '初次加载时间';
comment on COLUMN "tt_balance_item"."last_load_date" is '末次加载时间';
comment on COLUMN "tt_balance_item"."load_from" is '数据来源';

CREATE OR REPLACE TABLE "tt_balance_part" (
	"id" decimal(10,0),
	"part_no" varchar,
	"part_name" varchar,
	"part_quantity" decimal(8,2),
	"unit" varchar,
	"part_sale_price" decimal(10,2),
	"part_sale_amount" decimal(12,2),
	"part_cost_price" decimal(12,4),
	"part_cost_amount" decimal(12,2),
	"is_sgm_tag" decimal(1,0),
	"is_main_part" decimal(1,0),
	"storage_code" varchar,
	"bo_id" decimal(10,0),
	"bi_id" decimal(11,0),
	"balance_no" varchar,
	"asc_code" varchar,
	"ro_no" varchar,
	"is_valid" decimal(1,0),
	"first_load_date" timestamp,
	"last_load_date" timestamp,
	"load_from" varchar(30)
);
comment on TABLE "tt_balance_part" is '售后配件信息表';
comment on COLUMN "tt_balance_part"."id" is '配件ID';
comment on COLUMN "tt_balance_part"."part_no" is '配件代码';
comment on COLUMN "tt_balance_part"."part_name" is '配件名称';
comment on COLUMN "tt_balance_part"."part_quantity" is '配件数量';
comment on COLUMN "tt_balance_part"."unit" is '单位';
comment on COLUMN "tt_balance_part"."part_sale_price" is '配件销售单价';
comment on COLUMN "tt_balance_part"."part_sale_amount" is '配件销售金额';
comment on COLUMN "tt_balance_part"."part_cost_price" is '配件成本单价';
comment on COLUMN "tt_balance_part"."part_cost_amount" is '配件成本金额';
comment on COLUMN "tt_balance_part"."is_sgm_tag" is 'sgm标识';
comment on COLUMN "tt_balance_part"."is_main_part" is '是否主要配件';
comment on COLUMN "tt_balance_part"."storage_code" is '仓库代码';
comment on COLUMN "tt_balance_part"."bo_id" is '售后工单ID';
comment on COLUMN "tt_balance_part"."bi_id" is '售后项目ID';
comment on COLUMN "tt_balance_part"."balance_no" is '结算单号';
comment on COLUMN "tt_balance_part"."asc_code" is '经销商代码';
comment on COLUMN "tt_balance_part"."ro_no" is '工单号码';
comment on COLUMN "tt_balance_part"."is_valid" is '是否有效(1:有效，0:无效)';
comment on COLUMN "tt_balance_part"."first_load_date" is '初次加载时间';
comment on COLUMN "tt_balance_part"."last_load_date" is '末次加载时间';
comment on COLUMN "tt_balance_part"."load_from" is '数据来源';



CREATE OR REPLACE TABLE "td_asc" (
	"asc_code" varchar,
	"asc_name" varchar,
	"asc_full_nm" varchar,
	"asc_sap_code" varchar,
	"asc_warranty_code" varchar,
	"tax_no" varchar,
	"city_nm" varchar,
	"province_nm" varchar,
	"fmc_region_nm" varchar,
	"asc_build_date" timestamp,
	"asc_biz_status" varchar,
	"asc_biz_status_desc" varchar,
	"asc_biz_open_date" timestamp,
	"online_status" varchar,
	"online_status_desc" varchar,
	"online_date" timestamp,
	"asc_flg" varchar,
	"asc_star_grade" varchar,
	"asc_rank" varchar,
	"fmc_nm" varchar,
	"bank_nm" varchar,
	"bank_account_no" varchar,
	"biz_phone_no" varchar,
	"hotline_phone_no" varchar,
	"booking_phone_no" varchar,
	"email_addr" varchar,
	"asc_addr" varchar,
	"asc_zip_cd" varchar,
	"asc_brand" varchar,
	"eff_dt" timestamp,
	"end_dt" timestamp,
	"create_tmstp" timestamp,
	"update_tmstp" timestamp,
	"create_by" varchar,
	"update_by" varchar,
	"valid" decimal(1),
	"data_owner" varchar,
	"peer_group" varchar,
	"bac" varchar,
	"plant" varchar
);
comment on TABLE "td_asc" is '经销商信息';
comment on COLUMN "td_asc"."asc_code" is '经销商代码';
comment on COLUMN "td_asc"."asc_name" is 'ASC 名称';
comment on COLUMN "td_asc"."asc_full_nm" is 'ASC 全称';
comment on COLUMN "td_asc"."asc_sap_code" is 'ASC 在SAP中的代码';
comment on COLUMN "td_asc"."asc_warranty_code" is 'ASC索赔的代码';
comment on COLUMN "td_asc"."tax_no" is '税务登记号=duty number';
comment on COLUMN "td_asc"."city_nm" is '城市名称';
comment on COLUMN "td_asc"."province_nm" is '省名称';
comment on COLUMN "td_asc"."fmc_region_nm" is 'FMC的大区名称';
comment on COLUMN "td_asc"."asc_build_date" is 'ASC创建日期=created date';
comment on COLUMN "td_asc"."asc_biz_status" is '1 正式运行  2 开业准备  3 停业';
comment on COLUMN "td_asc"."asc_biz_status_desc" is '1 正式运行 2 开业准备 3 停业';
comment on COLUMN "td_asc"."asc_biz_open_date" is 'ASC开业日期= open date';
comment on COLUMN "td_asc"."online_status" is '0，未上线；1，已上线；2，上线中';
comment on COLUMN "td_asc"."online_status_desc" is '0，未上线；1，已上线；2，上线中';
comment on COLUMN "td_asc"."online_date" is '在线日期';
comment on COLUMN "td_asc"."asc_flg" is '0 ASC, 1非ASC';
comment on COLUMN "td_asc"."asc_star_grade" is 'ASC星级';
comment on COLUMN "td_asc"."asc_rank" is 'ASC级别';
comment on COLUMN "td_asc"."fmc_nm" is 'FMC名称';
comment on COLUMN "td_asc"."bank_nm" is 'ASC的银行名称';
comment on COLUMN "td_asc"."bank_account_no" is 'ASC银行帐号';
comment on COLUMN "td_asc"."biz_phone_no" is '业务电话号码';
comment on COLUMN "td_asc"."hotline_phone_no" is '热线电话号码';
comment on COLUMN "td_asc"."booking_phone_no" is '预定电话号码';
comment on COLUMN "td_asc"."email_addr" is '电子邮件地址';
comment on COLUMN "td_asc"."asc_addr" is 'ASC地址';
comment on COLUMN "td_asc"."asc_zip_cd" is 'ASC邮编号码';
comment on COLUMN "td_asc"."asc_brand" is 'ASC名牌Get the information from ServiceLink.TS_SGM_SYS_BRANDREGIONMAP';
comment on COLUMN "td_asc"."valid" is '是否有效，1有效 0无效';
comment on COLUMN "td_asc"."peer_group" is '用户自定义分组,来源于索赔运作提供的自定义分组数据';
comment on COLUMN "td_asc"."bac" is 'GWM BAC代码';
comment on COLUMN "td_asc"."plant" is '所属仓库';

USE vitas
CREATE SCHEMA mfg;
USE vitas.mfg;
CREATE OR REPLACE TABLE "ods_tm_vhcl" (
	"vin" varchar,
	"pvi" varchar,
	"plant_code" varchar,
	"import_flag" decimal(1,0),
	"vin_cntry_code" varchar,
	"vin_loc_code" varchar,
	"vin_mnfr_code" varchar,
	"vin_model_code" varchar,
	"vin_bdstl_code" varchar,
	"vin_rstrt_sys_typ_code" varchar,
	"vin_engine_typ_code" varchar,
	"vin_model_yr_code" varchar,
	"body_csn" varchar,
	"paint_csn" varchar,
	"asmbly_csn" varchar,
	"me_model_code" varchar,
	"prdn_order_date" timestamp,
	"prdn_order_time" timestamp,
	"brdcst_date" timestamp,
	"brdcst_time" timestamp,
	"buyoff_date" timestamp,
	"buyoff_time" timestamp,
	"care_ship_date" timestamp,
	"care_ship_time" timestamp,
	"ship_to_vdc_date" timestamp,
	"ship_to_vdc_time" timestamp,
	"sold_to_cust_date" timestamp,
	"scrpd_date" timestamp,
	"scrpd_time" timestamp,
	"pilot_vhcl_flag" varchar,
	"prdn_order_no" varchar,
	"drive" varchar,
	"md_brand_id" decimal(15,0),
	"md_model_id" decimal(20,0),
	"md_prdt_id" decimal(30,0),
	"gca_flag" varchar,
	"sap_mtr_no" varchar,
	"eds_id" decimal(15,0),
	"gsip_id" decimal(15,0),
	"gca_id" decimal(15,0),
	"is_effective" decimal(1,0),
	"src_create_date" timestamp,
	"src_update_date" timestamp,
	"first_load_date" timestamp,
	"last_load_date" timestamp,
	"load_from" varchar,
	"trns_typ" varchar,
	"detail_model" varchar,
	"nsc" varchar,
	"secu_code" varchar,
	"vdc_csn" varchar,
	"book" varchar,
	"eng_code" varchar,
	"color" varchar,
	"sales_odr" varchar,
	"eng_option_code" varchar,
	"odrsample" varchar,
	"model_z050" varchar,
	"model_z100" varchar,
	"model_z111" varchar,
	"odr_csn" varchar,
	"model_yr" varchar,
	"dl_first_load_time" timestamp,
	"dl_last_load_time" timestamp,
	"dl_is_valid" decimal(1,0),
	"dl_load_from" varchar,
	"ridkeycolumn" varchar
);
comment on TABLE "ods_tm_vhcl" is '车辆信息主表';
comment on COLUMN "ods_tm_vhcl"."vin" is '车辆唯一标识号';
comment on COLUMN "ods_tm_vhcl"."pvi" is 'PVI号码';
comment on COLUMN "ods_tm_vhcl"."plant_code" is '工厂代码(VIN码的第11位)';
comment on COLUMN "ods_tm_vhcl"."import_flag" is '进口标志';
comment on COLUMN "ods_tm_vhcl"."vin_cntry_code" is '国家标识(VIN码的第1位)';
comment on COLUMN "ods_tm_vhcl"."vin_loc_code" is '产地标识(VIN码的第2位)';
comment on COLUMN "ods_tm_vhcl"."vin_mnfr_code" is '厂商标识(VIN码的第3位)';
comment on COLUMN "ods_tm_vhcl"."vin_model_code" is '车型标识(VIN码的第4, 5位)';
comment on COLUMN "ods_tm_vhcl"."vin_bdstl_code" is '车身类型标识(VIN码的第6位)';
comment on COLUMN "ods_tm_vhcl"."vin_rstrt_sys_typ_code" is '车辆限制系统类型标识(VIN码的第7位)';
comment on COLUMN "ods_tm_vhcl"."vin_engine_typ_code" is '车辆发动机类型标识(VIN码的第8位)';
comment on COLUMN "ods_tm_vhcl"."vin_model_yr_code" is '车型年标识(VIN码的第10位)';
comment on COLUMN "ods_tm_vhcl"."body_csn" is '车身CSN (1digit+SS0+6 Digits)';
comment on COLUMN "ods_tm_vhcl"."paint_csn" is '油漆CSN (1digit+PP0+6 Digits)';
comment on COLUMN "ods_tm_vhcl"."asmbly_csn" is '总装CSN (1digit+GA0+6 Digits)';
comment on COLUMN "ods_tm_vhcl"."me_model_code" is '车型代码';
comment on COLUMN "ods_tm_vhcl"."prdn_order_date" is '生产订单传到GEPICS日期(01点)';
comment on COLUMN "ods_tm_vhcl"."prdn_order_time" is '生产订单传到GEPICS时间(01点)';
comment on COLUMN "ods_tm_vhcl"."brdcst_date" is '生成订单日期(05点)';
comment on COLUMN "ods_tm_vhcl"."brdcst_time" is '生成订单时间(05点)';
comment on COLUMN "ods_tm_vhcl"."buyoff_date" is '生产完成日期(80点)';
comment on COLUMN "ods_tm_vhcl"."buyoff_time" is '生产完成时间(80点)';
comment on COLUMN "ods_tm_vhcl"."care_ship_date" is '报交日期(90点)';
comment on COLUMN "ods_tm_vhcl"."care_ship_time" is '报交时间(90点)';
comment on COLUMN "ods_tm_vhcl"."ship_to_vdc_date" is 'VDC收车日期(95点)';
comment on COLUMN "ods_tm_vhcl"."ship_to_vdc_time" is 'VDC收车时间(95点)';
comment on COLUMN "ods_tm_vhcl"."sold_to_cust_date" is '车辆销售给客户日期';
comment on COLUMN "ods_tm_vhcl"."scrpd_date" is '报废日期';
comment on COLUMN "ods_tm_vhcl"."scrpd_time" is '报废日期时间';
comment on COLUMN "ods_tm_vhcl"."pilot_vhcl_flag" is '试生产车辆标记(GSIP Vehicle.pilot_veh)';
comment on COLUMN "ods_tm_vhcl"."prdn_order_no" is '生产订单号';
comment on COLUMN "ods_tm_vhcl"."drive" is '驱动';
comment on COLUMN "ods_tm_vhcl"."md_brand_id" is '品牌序列号';
comment on COLUMN "ods_tm_vhcl"."md_model_id" is '序列号';
comment on COLUMN "ods_tm_vhcl"."md_prdt_id" is '颜色序列号';
comment on COLUMN "ods_tm_vhcl"."gca_flag" is 'GCA检测标志';
comment on COLUMN "ods_tm_vhcl"."sap_mtr_no" is 'SAP物料号码';
comment on COLUMN "ods_tm_vhcl"."eds_id" is 'EDS中的车辆序列号';
comment on COLUMN "ods_tm_vhcl"."gsip_id" is '车辆GSIP系统序列号';
comment on COLUMN "ods_tm_vhcl"."gca_id" is '车辆GCA系统序列号';
comment on COLUMN "ods_tm_vhcl"."is_effective" is '数据记录是否有效';
comment on COLUMN "ods_tm_vhcl"."src_create_date" is '源系统记录创建时间';
comment on COLUMN "ods_tm_vhcl"."src_update_date" is '源系统记录最后更新时间';
comment on COLUMN "ods_tm_vhcl"."first_load_date" is '记录创建时间';
comment on COLUMN "ods_tm_vhcl"."last_load_date" is '记录最后更新时间';
comment on COLUMN "ods_tm_vhcl"."load_from" is '源系统名称';
comment on COLUMN "ods_tm_vhcl"."trns_typ" is '变速箱类型';
comment on COLUMN "ods_tm_vhcl"."detail_model" is '细分车型';
comment on COLUMN "ods_tm_vhcl"."nsc" is 'NSC';
comment on COLUMN "ods_tm_vhcl"."secu_code" is '安全代码';
comment on COLUMN "ods_tm_vhcl"."vdc_csn" is 'VDC CSN';
comment on COLUMN "ods_tm_vhcl"."book" is '车系';
comment on COLUMN "ods_tm_vhcl"."eng_code" is 'Package代码(和tm_package中的eng_cd关联)';
comment on COLUMN "ods_tm_vhcl"."color" is '颜色(和TM_COLOR中的OPTION_CODE关联)';
comment on COLUMN "ods_tm_vhcl"."sales_odr" is '销售订单';
comment on COLUMN "ods_tm_vhcl"."eng_option_code" is '发动机的配置代码';
comment on COLUMN "ods_tm_vhcl"."odrsample" is '订单样本';
comment on COLUMN "ods_tm_vhcl"."model_z050" is 'MODEL_Z050(来自GEPICS)';
comment on COLUMN "ods_tm_vhcl"."model_z100" is 'MODEL_Z100(来自GEPICS)';
comment on COLUMN "ods_tm_vhcl"."model_z111" is 'MODEL_Z111(来自GEPICS)';
comment on COLUMN "ods_tm_vhcl"."odr_csn" is 'order csn,订单CSN，即01点对应的CSN';
comment on COLUMN "ods_tm_vhcl"."model_yr" is '车型年';
comment on COLUMN "ods_tm_vhcl"."dl_first_load_time" is '初次创建时间';
comment on COLUMN "ods_tm_vhcl"."dl_last_load_time" is '末次更新时间';
comment on COLUMN "ods_tm_vhcl"."dl_is_valid" is '是否有效';
comment on COLUMN "ods_tm_vhcl"."dl_load_from" is '来源系统';

USE vitas;
