
--这是注释

--这也是注释
CREATE LOCAL TEMPORARY TABLE tmp_fake_tab_1(
		stat_dt date
) 
;
CREATE LOCAL TEMPORARY TABLE tmp_fake_tab_2(
		stat_dt date
) on commit preserve rows
;
CREATE LOCAL TEMPORARY TABLE tmp_fake_tab_3(
		stat_dt date
) on commit preserve rows
;

create local temporary table mgr_dim.mbl_second_channel_monday
(
	 stat_dt                 ,fst_chnl_cd             ,tdy_crd_cust_cnt       -- 日期
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               -- 新借贷款余额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           -- 贷款余额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   --申请用户数
	,etl_tms
	,7D_CRD_CUST_CNT         --近7日获客数
    ,7D_ADD_PRCP_BAL         --近7日净增 
	,7D_APL_CUST_CNT         --7天申请用户
	,7D_APV_PAS_CRD_CNT      --7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT --7天审批结案	                                           
)on commit preserve rows
;


CREATE local temporary table  tmp_neo_fake.it_is_there(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT '',

	
	ind_amt Numeric NOT NULL dEFaULT 0,  --注释
	cst_amt Numeric NOT NULL default 0,
	pft_amt Numeric NOT NULL DEFAULT 0, --哈哈
	new_7d_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	new_nat_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	old_7d_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	old_nat_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	etl_tms Timestamp NOT NULL DEFAULT "sysdate"(),
	year_add_prcp_bal Numeric NOT NULL DEFAULT 0
)on commit preserve rows;

CREATE local temporary table  tmp_neo_fake.it_is_forth(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT ''

)on commit preserve rows;

CREATE TABLE tmp_neo_fake.it_is_there_02(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT '',

	
	ind_amt Numeric NOT NULL dEFaULT 0,
	cst_amt Numeric NOT NULL default 0,
	pft_amt Numeric NOT NULL DEFAULT 0,
	new_7d_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	new_nat_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	old_7d_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	old_nat_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	etl_tms Timestamp NOT NULL DEFAULT "sysdate"(),
	year_add_prcp_bal Numeric NOT NULL DEFAULT 0, 
	CONSTRAINT pk_ceo_management_month PRIMARY KEY
	(stat_dt, fst_org_nbr, fst_crd_dt, fst_crd_situ_cd, fst_prod_cd, fst_chnl_cd, fst_mch_nbr)
)on commit preserve rows;

CREATE TABLE tmp_neo_fake.it_is_there_03(
	stat_dt Date NOT NULL DEFAULT '1900-01-01'::date,
	fst_org_nbr Varchar(10) NOT NULL DEFAULT '',
	fst_crd_dt Date Not NULL default '1900-01-01'::date,
	fst_crd_situ_cd Varchar(200) NOT NULL DEFAULT '',

	
	ind_amt Numeric NOT NULL dEFaULT 0,
	cst_amt Numeric NOT NULL default 0,
	pft_amt Numeric NOT NULL DEFAULT 0,
	new_7d_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	new_nat_actv_prcp_bal Numeric NOT NULL DEFAULt 0,
	old_7d_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	old_nat_actv_prcp_bal Numeric NOT NULL DEFAULT 0,
	etl_tms Timestamp NOT NULL DEFAULT "sysdate"(),
	year_add_prcp_bal Numeric NOT NULL DEFAULT 0, 
	CONSTRAINT pk_ceo_management_month PRIMARY KEY
	(stat_dt, fst_org_nbr, fst_crd_dt, fst_crd_situ_cd, fst_prod_cd, fst_chnl_cd, fst_mch_nbr)
)on commit preserve rows;

update dwa_fat.lmt_contract_his
	set end_dt=date('$v_date')
	where stat_dt in ctr_nbr
;

create local temporary table tmp_prob_ris_fee
on commit preserve rows as select * from etl_cfg.dbt_zh__map where 1>2;

insert INTO mgr_fat_mbl_first_page_channel_day(
	 stat_dt                 ,fst_chnl_cd             ,tdy_crd_cust_cnt       --日期
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               --新借贷款余额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           --贷款余额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   --申请用户数
	
	,7D_CRD_CUST_CNT         --近7日获客数
    ,7D_ADD_PRCP_BAL         --近7日净增 
	,7D_APL_CUST_CNT         --7天申请用户
	,7D_APV_PAS_CRD_CNT      --7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT --7天审批结案	                                           
);

select count * from ceo_management_day;

INSERT  into mgr_dim.mbl_second_channel_day

(
	 stat_dt                       --日期
	,new_dtrb_amt            ,rep_dtrb_amt            ,rpay_amt               --新借贷款余额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           --贷款余额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   --申请用户数
	
	,7D_CRD_CUST_CNT         --近7日获客数
    ,7D_ADD_PRCP_BAL         --近7日净增 
	,7D_APL_CUST_CNT         --7天申请用户
	,7D_APV_PAS_CRD_CNT      --7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT --天审批结案	                                           
)

select 
	 date'$v_date'           ,distinct fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,rep_dtrb_amt            ,distinct rpay_amt               --新借贷款余额
	,prcp_bal                ,tdy_add_prcp_bal        ,ovd_prcp_bal           --贷款余额
	,apl_cust_cnt            ,distinct tdy_apv_pas_cust        ,distinct vld_apv_cpl_cust_cnt   --申请用户数

	,case when sum(tdy_crd_cust_cnt)       --近7日获客数
	,sum(tdy_add_prcp_bal)       --近7日净增余额 
	,sum(apl_cust_cnt)           --7天申请用户数
	,sum(tdy_apv_pas_cust)       --天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   --天审批结案数
	
from mgr_fat.ceo_management_day
join 'table' on 'where'
where sum(stat_dt) > date'$v_date' - interval '7 day'
	and stat_dt <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;

delete * from mgr_fat.hello_me;
select count (*) from mgr_fat.management_day;
insert into mgr_dim.mbl_second_channel_day
(
	 stat_dt                 ,fst_chnl_cd                    --日期
	,new_dtrb_amt            ,rep_dtrb_amt                           --新借贷款余额
	,prcp_bal                ,tdy_add_prcp_bal                   --贷款余额
	,apl_cust_cnt            ,tdy_apv_pas_cust        ,vld_apv_cpl_cust_cnt   --申请用户数
	,etl_tms
	,7D_CRD_CUST_CNT         --近7日获客数
    ,7D_ADD_PRCP_BAL         --近7日净增 
	,7D_APL_CUST_CNT         --7天申请用户
	,7D_APV_PAS_CRD_CNT      --7天审批通过 
	,7D_VLD_APV_CPL_CUST_CNT --7天审批结案	                                           
)

select 
	 date'$v_date'           ,distinct fst_chnl_cd             ,tdy_crd_cust_cnt
	,new_dtrb_amt            ,distinct rep_dtrb_amt            ,rpay_amt               --新借贷款余额
	,prcp_bal                ,distinct tdy_add_prcp_bal        ,ovd_prcp_bal           --贷款余额
	,apl_cust_cnt            ,distinct tdy_apv_pas_cust        ,to_char(vld_apv_cpl_cust_cnt,'world')   --申请用户数
	
	,sum(tdy_crd_cust_cnt)       --近7日获客数 额 
	,sum(apl_cust_cnt)           --7天申请用户数
	,sum(tdy_apv_pas_cust)       --7天审批通过数
	,sum(vld_apv_cpl_cust_cnt)   --7天审批结案数

from mgr_fat.ceo_management_day 
join 
     ceo_management_month on a = b
outer	
where not between stat_dt > date'$v_date' - interval '7 day'
	 not    between a and b
	and to_char(stat_dt) <= date'$v_date'
  
group by
	date('$v_date'), fst_chnl_cd
;
select * from mgr_fat.ceo_management_day;