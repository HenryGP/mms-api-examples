#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, argparse, json
from automation_api_base import AutomationApiBase
from backup_api_base import BackupApiBase

def RedirectedRestore(automation_api, backup_api, source_cluster, destination_cluster):
    def get_clusters(cluster_name):
        clusters = {}
        autoConfig = automation_api.get_automation_config()
        for cluster in autoConfig["sharding"]:
            clusters[cluster["name"]]=[]
            for shard in cluster["shards"]:
                clusters[cluster["name"]].append(shard["_id"])
        try:
            return clusters[cluster_name]
        except KeyError:
            return []

    def validate_clusters(source_cluster, destination_cluster):
        validation = 0
        #Verify that the clusters exist
        if not len(get_clusters(source_cluster)):
            print "Incorrect source cluster name specified"
            validation-=1
        validation+=1
        if not len(get_clusters(destination_cluster)):
            print "Incorrect destination cluster name specified"
            validation-=1
        validation+=1
        validated = True if validation == 2 else False
        return validated

    def list_snapshots(snapshots):
        print "Available snapshots for cluster %s \n" % source_cluster
        
        for snapshot in snapshots:
            print snapshot
        

    if validate_clusters(source_cluster, destination_cluster):
        print "Source and destination cluster names validated"
        snapshots = backup_api.get_snapshots_cluster(source_cluster)
        list_snapshots(snapshots)
        print json.dumps(snapshots, indent=4, sort_keys=True)

    return
    


if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description='Redirected restore Demo')
    parser.add_argument('base_url', help="Base URL")
    parser.add_argument('group_id', help="Group ID")
    parser.add_argument('api_user', help="API User")
    parser.add_argument('api_key', help="API Key")
    args = parser.parse_args()
    '''

    base_url="http://192.168.1.100:8080"
    group_id="5ab7e900d72dd1375ada0bd1"
    api_user="admin"
    api_key="cf8fb22e-ced4-4fa4-bfbf-d29a4e2d7593"
    source_cluster="apiTestCluster"
    destination_cluster="apiTestCluster"

    automation_api = AutomationApiBase(base_url, base_url, group_id, api_user, api_key)
    backup_api = BackupApiBase(base_url, group_id, api_user, api_key)

    RedirectedRestore(automation_api, backup_api, source_cluster, destination_cluster)