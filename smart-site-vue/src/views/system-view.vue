<template>
  <div>
    <el-tree
      :data="checkSystemTree"
      node-key="systemId"
      default-expand-all
      :expand-on-click-node="false"
    >
      <span slot-scope="{ node, data }">
        <span :title="data.systemDescription">{{ data.systemName }}</span>
        <span>
          <el-button type="text" size="mini" @click="() => append(data)">
            Append
          </el-button>
          <el-button type="text" size="mini" @click="() => remove(data)">
            Delete
          </el-button>
          <el-button type="text" size="mini" @click="() => update(node, data)">
            Update
          </el-button>
        </span>
      </span>
    </el-tree>

    <vxe-modal
      v-model="showEdit"
      :title="selectAction ? '编辑&保存' : '新增&保存'"
      wsystemIdth="800"
      min-wsystemIdth="600"
      min-height="300"
      :loading="submitLoading"
      resize
      destroy-on-close
    >
      <template v-slot>
        <vxe-form
          :data="checkSystemNode"
          :rules="formRules"
          title-align="right"
          title-wsystemIdth="100"
          @submit="submitEvent"
        >
          <vxe-form-item title="编号" field="systemId" span="24">
            <template v-slot>
              <vxe-input
                v-model="checkSystemNode.systemId"
                placeholder="请输入当前检查体系编号"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item title="名称" field="systemName" span="24">
            <template v-slot>
              <vxe-input
                v-model="checkSystemNode.systemName"
                placeholder="请输入当前检查体系名称"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item title="父节点编号" field="preId" span="24">
            <template v-slot>
              <vxe-input
                v-model="checkSystemNode.preId"
                placeholder="请输入父节点编号称"
                :disabled="true"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>
          <vxe-form-item title="节点描述" field="systemDescription" span="24">
            <template v-slot>
              <vxe-input
                v-model="checkSystemNode.systemDescription"
                placeholder="请输入当前检查体系描述"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item align="center" span="24" titleAlign="left">
            <template v-slot>
              <vxe-button type="submit" status="primary">提交</vxe-button>
            </template></vxe-form-item
          >
        </vxe-form>
      </template>
    </vxe-modal>
  </div>
</template>

<script>
import service from "../utils/request.js";

export default {
  data() {
    return {
      checkSystemTree: [
        {
          systemId: 1,
          systemName: "一级 1",
          systemDescription: "这是一段描述",
          children: [
            {
              systemId: 4,
              systemName: "二级 1-1",
              systemDescription: "这是一段描述",
              children: [
                {
                  systemId: 9,
                  systemName: "三级 1-1-1",
                  systemDescription: "这是一段描述",
                },
                {
                  systemId: 10,
                  systemName: "三级 1-1-2",
                  systemDescription: "这是一段描述",
                },
              ],
            },
          ],
        },
        {
          systemId: 2,
          systemName: "一级 2",
          systemDescription: "这是一段描述",
          children: [
            {
              systemId: 5,
              systemName: "二级 2-1",
              systemDescription: "这是一段描述",
            },
            {
              systemId: 6,
              systemName: "二级 2-2",
              systemDescription: "这是一段描述",
            },
          ],
        },
        {
          systemId: 3,
          systemName: "一级 3",
          systemDescription: "这是一段描述",
          children: [
            {
              systemId: 7,
              systemName: "二级 3-1",
              systemDescription: "这是一段描述",
            },
            {
              systemId: 8,
              systemName: "二级 3-2",
              systemDescription: "这是一段描述",
            },
          ],
        },
      ],
      checkSystemNode: {
        systemId: null,
        systemName: null,
        preId: null,
        systemDescription: null,
      },
      formRules: {},
      showEdit: false,
      submitLoading: false,
      selectAction: false,
    };
  },

  mounted() {
    this.checkSystemTreeGet();
  },
  methods: {
    append(nodeData) {
      this.checkSystemNode = {
        systemId: "",
        systemName: "",
        preId: nodeData.systemId,
        systemDescription: "",
      };
      (this.selectAction = false), (this.showEdit = true);
      console.dir(nodeData);
    },
    update(node, nodeData) {
      this.checkSystemNode = {
        systemId: nodeData.systemId,
        systemName: nodeData.systemName,
        preId: node.parent.data.systemId,
        systemDescription: nodeData.systemDescription,
      };
      this.selectAction = true;
      this.showEdit = true;
      console.dir(nodeData);
    },

    remove(nodeData) {
      console.dir(nodeData);
      new Promise((resolve, reject) => {
        if (confirm("您确定要删除吗？")) {
          resolve();
        } else {
          reject();
        }
      })
        .then(() => {
          service({
            url: "/system/delete",
            data: {
              systemId: nodeData.systemId,
            },
          }).then(({ data }) => {
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.checkSystemTreeGet();
          });
        })
        .catch(() => {
          console.log("删除失败");
        });
    },

    submitEvent() {
      this.submitLoading = true;
      if (this.selectAction) {
        //编辑合约
        service({
          url: "/system/update",
          data: {
            systemId: this.checkSystemNode.systemId,
            systemName: this.checkSystemNode.systemName,
            preId: this.checkSystemNode.preId,
            systemDescription: this.checkSystemNode.systemDescription,
          },
        })
          .then(({ data }) => {
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.checkSystemTreeGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      } else {
        //新增合约
        service({
          url: "/system/create",
          data: {
            systemId: this.checkSystemNode.systemId,
            systemName: this.checkSystemNode.systemName,
            preId: this.checkSystemNode.preId,
            systemDescription: this.checkSystemNode.systemDescription,
          },
        })
          .then(({ data }) => {
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.checkSystemTreeGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      }
    },

    checkSystemTreeGet() {
      service({
        url: "/system/getTree",
      })
        .then(({ data }) => {
          console.log(data);
          this.checkSystemTree = data.tree;
        })
        .catch((e) => {});
    },
  },
};
</script>
